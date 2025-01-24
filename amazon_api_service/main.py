import atexit
import json
import os
import subprocess
import threading
import traceback
from datetime import datetime
from flask import Flask, request, jsonify, g
from logs.logger import logger
import hashlib
import time
from models.update_api import update_api
from models.create_api import create_api
from models.list_api import list_api
from apscheduler.schedulers.background import BackgroundScheduler
from util.automatic_configuration import automatic_configuration
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import REDIS_CONFIG
import redis

app = Flask(__name__)
redis_client = redis.Redis(**REDIS_CONFIG)
REDIS_KEY = "error_queue" # 存储错误信息的 Redis 键
# # 定义你想定时执行的函数
# def scheduled_task():
#     # 这里放入你想定时执行的代码
#     automatic_configuration()
#     app.logger.info("automatic_configuration is running...")
#
#
# # 设置调度器
# scheduler = BackgroundScheduler()
# # 添加定时任务，比如每10秒执行一次
# scheduler.add_job(scheduled_task, 'interval', seconds=60 * 60 * 1)
# scheduler.start()
#
# # 确保在应用关闭时停止调度器
# atexit.register(lambda: scheduler.shutdown())


# 验证函数
def verify_request(token, timestamp, secret_key):
    # 计算token
    calculated_token = hashlib.sha256((secret_key + str(timestamp) + secret_key).encode('utf-8')).hexdigest()
    return token == calculated_token


def validate_id(data):
    """检查数据中的ID是否有效"""
    if not data or 'ID' not in data or not data['ID']:
        return False
    if 'user' not in data or not data['user']:
        return False
    if 'db' not in data or not data['db']:
        return False
    return True

# 用于缓存发送次数和时间的字典
error_cache = {}

@app.before_request
def before_request():
    # 记录请求开始时间
    g.start_time = time.time()
    # 记录请求的基本信息
    g.request_data = {
        'method': request.method,
        'url': request.url,
        'headers': dict(request.headers),
        'data': request.get_data(as_text=True)
    }
    logger.info(f"Request started: {g.request_data}")


def send_error_email(error_message, method_name):
    """将错误信息和堆栈跟踪存储到 Redis 中，如果 Redis 失败则直接发送邮件"""
    try:
        # 获取完整的堆栈跟踪信息
        traceback_info = traceback.format_exc()

        # 如果堆栈跟踪信息不为空，则将其附加到错误消息中
        if traceback_info.strip() != "NoneType: None":
            error_message = f"{error_message}\n\nTraceback:\n{traceback_info}"

        # 将错误信息存储为字符串
        error_data = f"{datetime.now()}: Method {method_name} - {error_message}"

        # 尝试将错误信息推入 Redis 列表
        try:
            redis_client.lpush(REDIS_KEY, error_data)
            redis_client.expire(REDIS_KEY, 60 * 21)  # 设置过期时间为 20 分钟

            # 如果没有定时器，则启动一个定时器
            if not hasattr(send_error_email, 'timer'):
                send_error_email.timer = threading.Timer(60 * 20, check_and_send_summary_email)
                send_error_email.timer.start()
                logger.info("Timer started successfully.")
        except Exception as redis_error:
            # 如果 Redis 操作失败，直接发送邮件
            logger.error(f"Redis operation failed: {str(redis_error)}")
            send_email("Redis Error Notification", f"Redis operation failed: {str(redis_error)}\n\nError details:\n{error_data}")
    except Exception as e:
        logger.error(f"Failed to store error in Redis or send email: {str(e)}")


def check_and_send_summary_email():
    """检查 Redis 中的错误信息并发送汇总邮件"""
    logger.info("check_and_send_summary_email function called.")
    try:
        # 从 Redis 中获取所有错误信息
        error_messages = redis_client.lrange(REDIS_KEY, 0, -1)

        if not error_messages:
            logger.info("No errors to send.")
            if hasattr(send_error_email, 'timer'):
                send_error_email.timer.cancel()
                delattr(send_error_email, 'timer')
            return

        # 构建邮件内容
        subject = "Summary of Errors in API Calls"
        body = "The following errors occurred in the last 20 minutes:\n\n"
        for error in error_messages:
            body += f"{error.decode('utf-8')}\n"

        # 发送邮件
        send_email(subject, body)

        # 清空 Redis 中的错误信息
        redis_client.delete(REDIS_KEY)

        # 清除定时器
        if hasattr(send_error_email, 'timer'):
            send_error_email.timer.cancel()
            delattr(send_error_email, 'timer')
    except Exception as e:
        logger.error(f"Failed to check Redis or send summary email: {str(e)}")
        send_email("Redis Error Notification", f"Failed to check Redis or send summary email: {str(e)}")


def send_email(subject, body):
    """发送邮件"""
    # 邮件配置
    SENDER_EMAIL = "wanghequan@deepbi.com"  # 发件人邮箱
    RECEIVER_EMails = ["wanghequan@deepbi.com", "lipengcheng@deepbi.com"]  # 收件人邮箱列表
    EMAIL_PASSWORD = "tpa15CVg4pfBL1yK"  # 邮箱授权码
    SMTP_SERVER = "smtp.feishu.cn"  # SMTP 服务器地址
    SMTP_PORT = 587  # SMTP 端口
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = ", ".join(RECEIVER_EMails)
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # 启用 TLS 加密
            server.login(SENDER_EMAIL, EMAIL_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMails, msg.as_string())
            logger.info(f"Summary email sent successfully to {', '.join(RECEIVER_EMails)}")
    except Exception as email_error:
        logger.error(f"Failed to send summary email: {str(email_error)}")


@app.after_request
def after_request(response):
    # 计算请求处理时间
    elapsed_time = time.time() - g.start_time
    # 记录响应的基本信息
    log_data = {
        'method': g.request_data['method'],
        'url': g.request_data['url'],
        'status': response.status,
        'text': response.get_data(as_text=True),
        'elapsed_time': elapsed_time,
        'headers': g.request_data['headers'],
        'data': g.request_data['data']
    }
    logger.info(f"Request finished: {log_data}")
    if response.status_code != 200:
        # 获取 JSON 数据
        response_data = g.request_data['data']

        # 如果 response_data 是字符串形式的 JSON，先解析为字典
        if isinstance(response_data, str):
            response_data = json.loads(response_data)

        # 格式化 JSON 数据，确保中文显示正常
        formatted_data = json.dumps(response_data, ensure_ascii=False)
        error_message = f"Request to {g.request_data['url']} failed with status {response.status_code}.\nResponse Text: {response.get_data(as_text=True)}\ndata:{formatted_data}"
        method_name = f"{g.request_data['method']} {g.request_data['url']}"
        # 调用 send_error_email 方法发送错误邮件
        send_error_email(error_message, method_name)
    return response

@app.route('/api/data/list', methods=['POST'])
async def handle_list():
    # 获取请求头和请求体
    token = request.headers.get('token')
    timestamp = request.headers.get('timestamp')
    data = request.get_json()
    print(data)
    # 验证请求头
    secret_key = "69c5fcebaa65b560eaf06c3fbeb481ae44b8d618"  # 测试环境的秘钥, 根据环境配置选择秘钥
    if not verify_request(token, timestamp, secret_key):
        return jsonify({"error": "Unauthorized"}), 401
    if not data.get("text") or data["text"] == "":
        return jsonify({"status": 404, "error": "The 'text' field cannot be an empty string."})
    result = await list_api(data)  # 获取 AsyncResult 对象
    code, info, e = result  # 从结果中解包任务返回的值（同步阻塞，等待任务完成）
    if code == 200:
        return jsonify({"status": 200, "info": info, "error": e})
    else:
        # 获取 JSON 数据
        response_data = g.request_data['data']

        # 如果 response_data 是字符串形式的 JSON，先解析为字典
        if isinstance(response_data, str):
            response_data = json.loads(response_data)

        # 格式化 JSON 数据，确保中文显示正常
        formatted_data = json.dumps(response_data, ensure_ascii=False)
        error_message = f"Request to {g.request_data['url']} failed .\nResponse data:{formatted_data}.error:{str(e)}"
        method_name = f"{g.request_data['method']} {g.request_data['url']}"
        # 调用 send_error_email 方法发送错误邮件
        send_error_email(error_message, method_name)
        return jsonify({"status": code, "info": info, "error": str(e)})

@app.route('/api/data/create', methods=['POST'])
async def handle_insert():
    current_time = datetime.now()

    # 打印当前时间（默认格式：年-月-日 时:分:秒.毫秒）
    print('收到请求：',current_time)
    # 获取请求头和请求体
    token = request.headers.get('token')
    timestamp = request.headers.get('timestamp')
    data = request.get_json()
    print(data)
    # 验证请求头
    secret_key = "69c5fcebaa65b560eaf06c3fbeb481ae44b8d618"  # 测试环境的秘钥, 根据环境配置选择秘钥
    if not verify_request(token, timestamp, secret_key):
        return jsonify({"error": "Unauthorized"}), 401
    if not data.get("text") or data["text"] == "":
        return jsonify({"status": 404, "error": "The 'text' field cannot be an empty string."})
    result = await create_api(data)  # 获取 AsyncResult 对象
    code, id, e = result  # 从结果中解包任务返回的值（同步阻塞，等待任务完成）
    if code == 200:
        return jsonify({"status": 200, "id": id, "error": e})
    else:
        # 获取 JSON 数据
        response_data = g.request_data['data']

        # 如果 response_data 是字符串形式的 JSON，先解析为字典
        if isinstance(response_data, str):
            response_data = json.loads(response_data)
        print(response_data)
        if 'require' in response_data and response_data['require'] == 'create' and response_data['position'] == 'sku':
            print(error_cache)
            current_time = time.time()
            cache_key = f"{g.request_data['url']}_create_error"

            # 检查缓存是否存在
            if cache_key in error_cache:
                error_info = error_cache[cache_key]
                # 判断是否在 30 分钟内且发送次数未超过 3 次
                if (current_time - error_info['last_sent_time']) < 1800 and error_info['count'] < 3:
                    # 更新计数和时间
                    print("error_info['count']:"+str(error_info['count']))
                    error_info['count'] += 1
                    error_info['last_sent_time'] = current_time
                    error_cache[cache_key] = error_info
                elif (current_time - error_info['last_sent_time']) >= 1800:
                    # 30 分钟过后重置计数和时间
                    error_cache[cache_key] = {'count': 1, 'last_sent_time': current_time}
                else:
                    return jsonify({"status": code, "error": str(e)})
            else:
                # 添加到缓存中，首次发送
                error_cache[cache_key] = {'count': 1, 'last_sent_time': current_time}
        # 格式化 JSON 数据，确保中文显示正常
        formatted_data = json.dumps(response_data, ensure_ascii=False)
        error_message = f"Request to {g.request_data['url']} failed .\nResponse data:{formatted_data}.error:{str(e)}"
        method_name = f"{g.request_data['method']} {g.request_data['url']}"
        # 调用 send_error_email 方法发送错误邮件
        send_error_email(error_message, method_name)
        return jsonify({"status": code, "id": id, "error": str(e)})


@app.route('/api/data/update', methods=['POST'])
async def handle_update():
    # 获取请求头和请求体
    token = request.headers.get('token')
    timestamp = request.headers.get('timestamp')
    data = request.get_json()
    current_time = datetime.now()

    # 打印当前时间（默认格式：年-月-日 时:分:秒.毫秒）
    print('收到请求：',current_time)
    # 验证请求头
    secret_key = "69c5fcebaa65b560eaf06c3fbeb481ae44b8d618"  # 测试环境的秘钥, 根据环境配置选择秘钥
    if not verify_request(token, timestamp, secret_key):
        return jsonify({"status":401,"error":"Unauthorized"})
    if not validate_id(data):
        return jsonify({"status":400,"error":"Invalid or missing ID"})
    # 调用 update_api 并处理返回值
    result = await update_api(data)  # 获取 AsyncResult 对象
    code, e = result  # 从结果中解包任务返回的值（同步阻塞，等待任务完成）
    if code == 200:
        return jsonify({"status":200,"error":e})
    else:
        # 获取 JSON 数据
        response_data = g.request_data['data']

        # 如果 response_data 是字符串形式的 JSON，先解析为字典
        if isinstance(response_data, str):
            response_data = json.loads(response_data)
            # 检查是否需要发送错误邮件
        if 'require' in response_data and response_data['require'] == 'create':
            print(error_cache)
            current_time = time.time()
            cache_key = f"{g.request_data['url']}_create_error"

            # 检查缓存是否存在
            if cache_key in error_cache:
                error_info = error_cache[cache_key]
                # 判断是否在 30 分钟内且发送次数未超过 3 次
                if (current_time - error_info['last_sent_time']) < 1800 and error_info['count'] < 3:
                    # 更新计数和时间
                    print("error_info['count']:"+str(error_info['count']))
                    error_info['count'] += 1
                    error_info['last_sent_time'] = current_time
                    error_cache[cache_key] = error_info
                elif (current_time - error_info['last_sent_time']) >= 1800:
                    # 30 分钟过后重置计数和时间
                    error_cache[cache_key] = {'count': 1, 'last_sent_time': current_time}
                else:
                    return jsonify({"status": code, "error": str(e)})
            else:
                # 添加到缓存中，首次发送
                error_cache[cache_key] = {'count': 1, 'last_sent_time': current_time}
        # 格式化 JSON 数据，确保中文显示正常
        formatted_data = json.dumps(response_data, ensure_ascii=False)
        error_message = f"Request to {g.request_data['url']} failed .\nResponse data:{formatted_data}.error:{str(e)}"
        method_name = f"{g.request_data['method']} {g.request_data['url']}"
        # 调用 send_error_email 方法发送错误邮件
        send_error_email(error_message, method_name)
        return jsonify({"status":code,"error": str(e)})


@app.route('/api/data/delete', methods=['POST'])
def handle_delete():
    # 获取请求头和请求体
    token = request.headers.get('token')
    timestamp = request.headers.get('timestamp')
    data = request.get_json()

    # 验证请求头
    secret_key = "69c5fcebaa65b560eaf06c3fbeb481ae44b8d618"  # 测试环境的秘钥, 根据环境配置选择秘钥
    if not verify_request(token, timestamp, secret_key):
        return jsonify({"error": "Unauthorized"}), 401

    # 处理删除数据的逻辑
    # 在此处添加处理删除数据的逻辑
    return jsonify({"message": "Delete data received"}), 200


if __name__ == '__main__':
    automatic_configuration()
    app.run(debug=False, host='0.0.0.0', port=8009, threaded=True)
