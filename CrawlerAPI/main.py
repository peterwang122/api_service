import asyncio
import os
from datetime import datetime
import traceback
from sanic import Sanic
from sanic.response import json as json_sanic
import json
from sanic.request import Request
import time
import hashlib
from log.logger_config import logger
import json as json_lib
import atexit
import smtplib
import redis
from config import REDIS_CONFIG
from util.list_api import list_api
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


app = Sanic(__name__)
redis_client = redis.Redis(db=12,**REDIS_CONFIG)
# 验证函数
# 定义双队列映射
TASK_QUEUES = {
    "SearchtermCrawlerAsin": ["high_priority_queue_NA", "high_priority_queue_EU", "high_priority_queue_FE"],
    "CrawlerAsin": ["low_priority_queue"]  # 修改为列表格式
}


# 新增地区映射判断函数
def determine_queue(market):
    """根据market参数确定地区队列"""
    market = str(market).upper()
    na_markets = {"US", "MX", "CA", "BR"}
    fe_markets = {"JP", "AU", "SG"}

    if market in na_markets:
        return "high_priority_queue_NA"
    if market in fe_markets:
        return "high_priority_queue_FE"
    return "high_priority_queue_EU"  # 其他情况默认EU队列


def verify_request(token, timestamp, secret_key):
    """请求验证函数"""
    calculated_token = hashlib.sha256(
        (secret_key + str(timestamp) + secret_key).encode('utf-8')
    ).hexdigest()
    return token == calculated_token


@app.before_server_start
async def setup(app, _):
    """服务启动初始化"""
    app.ctx.running = asyncio.Event()
    app.ctx.running.set()

    # 初始化任务处理器跟踪
    app.ctx.processing_tasks = {}
    app.ctx.processing_lock = asyncio.Lock()

    # 只启动有任务的队列处理器
    all_queues = []
    for q in TASK_QUEUES.values():
        all_queues.extend(q if isinstance(q, list) else [q])

    for queue in set(all_queues):
        queue = str(queue)
        if redis_client.llen(queue) > 0:
            app.add_task(start_processor(queue))

    app.config.REQUEST_TIMEOUT = 1800
    app.config.RESPONSE_TIMEOUT = 1800


async def start_processor(queue_name: str):
    """启动任务处理器并跟踪状态"""
    async with app.ctx.processing_lock:
        if queue_name in app.ctx.processing_tasks:
            return

        processor = app.add_task(task_processor(queue_name))
        app.ctx.processing_tasks[queue_name] = processor
        print(f"启动 {queue_name} 的任务处理器")


async def task_processor(queue_name: str):
    """动态任务处理器"""
    processing_queue = f"{queue_name}:processing"
    try:
        while app.ctx.running.is_set():
            try:
                task_data = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: redis_client.rpoplpush(queue_name, processing_queue)
                )

                if not task_data:
                    await asyncio.sleep(0.5)
                    continue

                data = json.loads(task_data)
                print(f"[{queue_name}] 开始处理任务: {data}")

                await list_api(data)

                await asyncio.get_event_loop().run_in_executor(
                    None, redis_client.lrem, processing_queue, 1, task_data
                )
                print(f"[{queue_name}] 任务完成: {data}")

            except Exception as e:
                print(f"任务处理失败: {str(e)}")
                await asyncio.get_event_loop().run_in_executor(
                    None, lambda: redis_client.rpush(queue_name, task_data)
                )
                await asyncio.get_event_loop().run_in_executor(
                    None, redis_client.lrem, processing_queue, 1, task_data
                )
            finally:
                # 检查队列是否为空
                current_count = redis_client.llen(queue_name)
                if current_count == 0:
                    print(f"{queue_name} 队列已空，停止处理")
                    break
                await asyncio.sleep(0.1)

    except asyncio.CancelledError:
        processing_tasks = await asyncio.get_event_loop().run_in_executor(
            None, redis_client.lrange, processing_queue, 0, -1
        )
        for task in processing_tasks:
            await asyncio.get_event_loop().run_in_executor(
                None, lambda: redis_client.rpush(queue_name, task)
            )
        await asyncio.get_event_loop().run_in_executor(
            None, redis_client.delete, processing_queue
        )
        print(f"已恢复{len(processing_tasks)}个未完成任务到{queue_name}")
    finally:
        async with app.ctx.processing_lock:
            if queue_name in app.ctx.processing_tasks:
                del app.ctx.processing_tasks[queue_name]


@app.before_server_stop
async def teardown(app, _):
    """增强的关闭处理"""
    app.ctx.running.clear()

    # 获取所有任务并等待完成
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    for task in tasks:
        task.cancel()

    # 增强的等待逻辑
    try:
        await asyncio.wait_for(
            asyncio.gather(*tasks, return_exceptions=True),
            timeout=5
        )
    except asyncio.TimeoutError:
        print("部分任务未能在超时时间内完成")
    finally:
        await asyncio.sleep(1)  # 确保所有资源释放


async def handle_retry(queue_name, task_data):
    """增强的重试逻辑"""
    try:
        current_length = await asyncio.get_event_loop().run_in_executor(
            None, redis_client.llen, queue_name
        )
        if current_length < 1000:
            await asyncio.get_event_loop().run_in_executor(
                None, lambda: redis_client.rpush(queue_name, task_data)
            )
            print(f"任务重新入队: {task_data.decode()}")
    except Exception as e:
        print(f"重试入队失败: {str(e)}")


@app.exception(Exception)
async def global_exception_handler(request, exception):
    """全局异常处理"""
    error_msg = f"请求 {request.url} 出错: {str(exception)}"
    print(error_msg)
    error_trace = traceback.format_exc()
    print(error_trace)
    return json_sanic({"error": error_msg}, status=500)


@app.route('/api/data/list', methods=['POST'])
async def handle_task(request: Request):
    """任务提交接口"""
    # 身份验证
    secret_key = "69c5fcebaa65b560eaf06c3fbeb481ae44b8d618"
    if not verify_request(
            request.headers.get('token'),
            request.headers.get('timestamp'),
            secret_key
    ):
        return json_sanic({"error": "认证失败"}, status=401)

    # 数据校验
    data = request.json
    if not data.get("text"):
        return json_sanic({"error": "text字段不能为空"}, status=400)

    # 任务类型校验
    task_type = data.get("position")
    if task_type not in TASK_QUEUES:
        return json_sanic({
            "status": 400,
            "error": "无效任务类型",
            "allowed_types": list(TASK_QUEUES.keys())
        }, status=400)

    # 确定目标队列
    if task_type == "SearchtermCrawlerAsin":
        if not data.get("market"):
            return json_sanic({"error": "高优先级任务必须包含market参数"}, status=400)
        target_queue = determine_queue(data["market"])
    else:
        target_queue = TASK_QUEUES[task_type][0] if isinstance(TASK_QUEUES[task_type], list) else TASK_QUEUES[task_type]

    # 检查重复任务
    task_json = json.dumps(data)
    check_queues = [str(q) for q in
                    (TASK_QUEUES[task_type] if isinstance(TASK_QUEUES[task_type], list) else [TASK_QUEUES[task_type]])]

    for q in check_queues:
        try:
            existing_tasks = redis_client.lrange(q, 0, -1)
            if any(task.decode('utf-8') == task_json for task in existing_tasks):
                return json_sanic({
                    "status": 200,
                    "info": "任务已存在",
                    "queue": target_queue
                })
        except redis.exceptions.DataError as e:
            print(f"队列检查错误: {str(e)}")
            continue

    try:
        target_queue = str(target_queue)
        redis_client.rpush(target_queue, task_json)

        # 提交后检查是否需要启动处理器
        async with app.ctx.processing_lock:
            if target_queue not in app.ctx.processing_tasks:
                app.add_task(start_processor(target_queue))

    except redis.exceptions.DataError as e:
        return json_sanic({
            "error": f"任务提交失败: {str(e)}",
            "queue": target_queue
        }, status=500)

    return json_sanic({
        "status": 200,
        "info": "任务提交成功",
        "queue": target_queue,
        "position": redis_client.llen(target_queue)
    })

# 队列监控接口
@app.route('/queues/status', methods=['GET'])
async def queue_monitor(request: Request):
    """队列状态查询（修复类型错误版）"""
    status = {}
    # 获取所有实际队列名称（展开列表型配置）
    all_queues = []
    for q in TASK_QUEUES.values():
        all_queues.extend(q if isinstance(q, list) else [q])

    # 为每个物理队列单独记录状态
    for queue in set(all_queues):
        # 安全处理二进制数据
        oldest = redis_client.lindex(queue, 0)
        newest = redis_client.lindex(queue, -1)

        status[queue] = {
            "pending_tasks": redis_client.llen(queue),
            "oldest_task": oldest.decode('utf-8') if oldest else None,
            "newest_task": newest.decode('utf-8') if newest else None
        }

    return json_sanic(status)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
