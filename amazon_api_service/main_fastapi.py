import atexit
import json
import os
import subprocess
import threading
from datetime import datetime
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, Response
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
from configuration.path import get_config_path
from pydantic import BaseModel

app = FastAPI()

# 定义你想定时执行的函数
def scheduled_task():
    automatic_configuration()
    logger.info("automatic_configuration is running...")

# 设置调度器
scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_task, 'interval', seconds=60 * 60 * 1)
scheduler.start()

# 确保在应用关闭时停止调度器
atexit.register(lambda: scheduler.shutdown())

# 验证函数
def verify_request(token: str, timestamp: str, secret_key: str) -> bool:
    calculated_token = hashlib.sha256((secret_key + str(timestamp) + secret_key).encode('utf-8')).hexdigest()
    return token == calculated_token

def validate_id(data: dict) -> bool:
    if not data or 'ID' not in data or not data['ID']:
        return False
    if 'user' not in data or not data['user']:
        return False
    if 'db' not in data or not data['db']:
        return False
    return True

# 用于缓存发送次数和时间的字典
error_cache = {}

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    request_data = {
        'method': request.method,
        'url': str(request.url),
        'headers': dict(request.headers),
        'data': await request.body()
    }
    logger.info(f"Request started: {request_data}")

    # 调用下一个中间件或路由处理函数
    response = await call_next(request)

    # 计算请求处理时间
    elapsed_time = time.time() - start_time

    # 获取响应体内容
    response_body = b""
    async for chunk in response.body_iterator:
        response_body += chunk

    # 重新创建响应对象
    new_response = Response(content=response_body, status_code=response.status_code, headers=dict(response.headers))

    # 记录响应的基本信息
    log_data = {
        'method': request_data['method'],
        'url': request_data['url'],
        'status': response.status_code,
        'text': response_body.decode('utf-8'),
        'elapsed_time': elapsed_time,
        'headers': request_data['headers'],
        'data': request_data['data'].decode('utf-8')
    }
    logger.info(f"Request finished: {log_data}")

    return new_response

def send_error_email(error_message: str, method_name: str):
    sender_email = "wanghequan@deepbi.com"
    receiver_emails = ["wanghequan@deepbi.com", "lipengcheng@deepbi.com"]
    password = "tpa15CVg4pfBL1yK"
    smtp_server = "smtp.feishu.cn"
    smtp_port = 587

    subject = f"Error in {method_name} API Call"
    body = f"An error occurred in method {method_name}: {error_message}"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = ", ".join(receiver_emails)
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_emails, msg.as_string())
            print(f"Error email sent successfully to {', '.join(receiver_emails)}")
    except Exception as email_error:
        print(f"Failed to send error email: {str(email_error)}")

class ListRequest(BaseModel):
    text: str

@app.post('/api/data/list')
async def handle_list(request: Request):
    token = request.headers.get('token')
    timestamp = request.headers.get('timestamp')
    data = await request.json()
    secret_key = "69c5fcebaa65b560eaf06c3fbeb481ae44b8d618"
    if not verify_request(token, timestamp, secret_key):
        raise HTTPException(status_code=401, detail="Unauthorized")
    if not data.get("text") or data["text"] == "":
        raise HTTPException(status_code=404, detail="The 'text' field cannot be an empty string.")
    result = list_api(data)
    code, info, e = result
    if code == 200:
        return JSONResponse(content={"status": 200, "info": info, "error": e})
    else:
        response_data = await request.body()
        if isinstance(response_data, bytes):
            response_data = response_data.decode('utf-8')
        if isinstance(response_data, str):
            response_data = json.loads(response_data)
        formatted_data = json.dumps(response_data, ensure_ascii=False)
        error_message = f"Request to {request.url} failed .\nResponse data:{formatted_data}"
        method_name = f"{request.method} {request.url}"
        send_error_email(error_message, method_name)
        return JSONResponse(content={"status": code, "info": info, "error": str(e)})

class CreateRequest(BaseModel):
    text: str

@app.post('/api/data/create')
async def handle_insert(request: Request):
    current_time = datetime.now()
    print('收到请求：', current_time)
    token = request.headers.get('token')
    timestamp = request.headers.get('timestamp')
    data = await request.json()
    secret_key = "69c5fcebaa65b560eaf06c3fbeb481ae44b8d618"
    if not verify_request(token, timestamp, secret_key):
        raise HTTPException(status_code=401, detail="Unauthorized")
    if not data.get("text") or data["text"] == "":
        raise HTTPException(status_code=404, detail="The 'text' field cannot be an empty string.")
    result = create_api(data)
    code, id, e = result
    if code == 200:
        return JSONResponse(content={"status": 200, "id": id, "error": e})
    else:
        response_data = await request.body()
        if isinstance(response_data, bytes):
            response_data = response_data.decode('utf-8')
        if isinstance(response_data, str):
            response_data = json.loads(response_data)
        print(response_data)
        if 'require' in response_data and response_data['require'] == 'create' and response_data['position'] == 'sku':
            print(111)
            print(error_cache)
            current_time = time.time()
            cache_key = f"{request.url}_create_error"
            if cache_key in error_cache:
                error_info = error_cache[cache_key]
                if (current_time - error_info['last_sent_time']) < 1800 and error_info['count'] < 3:
                    print("error_info['count']:" + str(error_info['count']))
                    error_info['count'] += 1
                    error_info['last_sent_time'] = current_time
                    error_cache[cache_key] = error_info
                elif (current_time - error_info['last_sent_time']) >= 1800:
                    error_cache[cache_key] = {'count': 1, 'last_sent_time': current_time}
                else:
                    return JSONResponse(content={"status": code, "error": str(e)})
            else:
                error_cache[cache_key] = {'count': 1, 'last_sent_time': current_time}
        formatted_data = json.dumps(response_data, ensure_ascii=False)
        error_message = f"Request to {request.url} failed .\nResponse data:{formatted_data}"
        method_name = f"{request.method} {request.url}"
        send_error_email(error_message, method_name)
        return JSONResponse(content={"status": code, "id": id, "error": str(e)})

class UpdateRequest(BaseModel):
    ID: str
    user: str
    db: str

@app.post('/api/data/update')
async def handle_update(request: Request):
    token = request.headers.get('token')
    timestamp = request.headers.get('timestamp')
    data = await request.json()
    current_time = datetime.now()
    print('收到请求：', current_time)
    secret_key = "69c5fcebaa65b560eaf06c3fbeb481ae44b8d618"
    if not verify_request(token, timestamp, secret_key):
        raise HTTPException(status_code=401, detail="Unauthorized")
    if not validate_id(data):
        raise HTTPException(status_code=400, detail="Invalid or missing ID")
    result = await update_api(data)
    code, e = result
    if code == 200:
        return JSONResponse(content={"status": 200, "error": e})
    else:
        return JSONResponse(content={"status": code, "error": str(e)})

@app.post('/api/data/delete')
async def handle_delete(request: Request):
    token = request.headers.get('token')
    timestamp = request.headers.get('timestamp')
    data = await request.json()
    secret_key = "69c5fcebaa65b560eaf06c3fbeb481ae44b8d618"
    if not verify_request(token, timestamp, secret_key):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return JSONResponse(content={"message": "Delete data received"}, status_code=200)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8009)