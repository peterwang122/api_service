import asyncio
import functools
from datetime import datetime
import logging
import aiohttp
import json
from functools import wraps
from time import sleep
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
from collections.abc import Iterable
from ad_api.base import Marketplaces
from logs.logger import logger
from util.common import get_ad_my_credentials
from concurrent.futures import ThreadPoolExecutor
from util.proxies import ProxyManager
from config import REDIS_CONFIG
import redis


# 假设你的基础API类
class BaseApi:
    def __init__(self, db, brand, market):
        self.brand = brand
        self.market = market
        self.db = db
        # self.executor = ThreadPoolExecutor()
        # self.credentials, self.access_token = self.load_credentials()
        self.attempts_time = 5
        self.proxy_manager = ProxyManager()
        self.redis_client = redis.Redis(**REDIS_CONFIG)  # 使用 config 中的 Redis 配置

    async def load_credentials(self):
        # # 假设这个方法是通用的，可以直接在这里实现
        # my_credentials, access_token = await get_ad_my_credentials(self.db, self.market, self.brand)
        # return my_credentials, access_token
        # 生成缓存键
        cache_key = f"credentials:{self.db}_{self.market}_{self.brand}"

        # 尝试从 Redis 缓存中获取数据
        cached_data = self.redis_client.get(cache_key)
        if cached_data:
            # 如果缓存中有数据，直接返回
            my_credentials, access_token = json.loads(cached_data)
            return my_credentials, access_token

        # 如果缓存中没有数据，从数据库或其他来源获取
        my_credentials, access_token,expires_in = await get_ad_my_credentials(self.db, self.market, self.brand)

        # 将结果存入 Redis 缓存
        self.redis_client.set(cache_key, json.dumps((my_credentials, access_token)), ex=expires_in)  # 设置缓存过期时间为 1 小时

        return my_credentials, access_token

    def log(self, message, level=logging.INFO):
        """
        记录日志，支持动态日志级别。
        :param message: 日志消息
        :param level: 日志级别，默认为 INFO
        """
        logger.log(level, message)

    async def wait_time(self):
        wait_time = random.randint(10, 20)
        self.log(f"Waiting for {wait_time} seconds before retrying...")
        await asyncio.sleep(wait_time)

    async def send_error_email(self, error_message, method_name):
        """发送错误邮件"""
        sender_email = "wanghequan@deepbi.com"  # 你的飞书邮箱地址
        receiver_emails = ["wanghequan@deepbi.com", "lipengcheng@deepbi.com"]  # 收件人的邮箱地址列表
        password = "tpa15CVg4pfBL1yK"  # 你的飞书邮箱授权码
        smtp_server = "smtp.feishu.cn"  # 飞书的 SMTP 服务器地址
        smtp_port = 587  # 使用 TLS 加密（端口 587）

        subject = f"Error in {method_name} API Call"
        body = f"An error occurred in method {method_name}: {error_message}"

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = ", ".join(receiver_emails)  # 多个收件人，用逗号分隔
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()  # 启用 TLS 加密
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_emails, msg.as_string())  # 发送邮件到多个收件人
                print(f"Error email sent successfully to {', '.join(receiver_emails)}")
        except Exception as email_error:
            print(f"Failed to send error email: {str(email_error)}")

    async def make_request(self, api_class, method_name, *args, **kwargs):
        self.credentials, self.access_token = await self.load_credentials()
        current_time = datetime.now()

        # 打印当前时间（默认格式：年-月-日 时:分:秒.毫秒）
        print('向亚马逊请求前：', current_time)
        attempts = 0
        result = None
        while attempts < self.attempts_time:
            try:
                self.log(
                    f"Attempting to call {method_name} with args: {args}, kwargs: {kwargs}. Attempt {attempts + 1}")

                # 动态创建 API 类的实例
                api_instance = api_class(
                    credentials=self.credentials,
                    marketplace=Marketplaces[self.market.upper()],
                    access_token=self.access_token,
                    proxies=self.proxy_manager.get_proxies(self.market),
                    debug=True
                )

                # 获取目标方法
                method = getattr(api_instance, method_name)

                # 异步执行同步方法
                result = method(**kwargs)# 1-2s
                # result = await asyncio.get_event_loop().run_in_executor(
                #     self.executor,functools.partial(method, **kwargs)
                # )

                if result and result.payload:
                    self.log(f"{method_name} success. Payload: {result.payload}")
                    return result.payload
                else:
                    self.log(
                        f"{method_name} failed or returned invalid payload: {result.payload if result else 'None'}")
                    await self.wait_time()
                    res = result.payload
                    attempts += 1

            except Exception as e:
                if attempts == self.attempts_time - 1:
                    self.log(f"Exception occurred in {method_name}: {str(e)}")
                    # 如果是最后一次尝试，直接抛出异常
                    # await self.send_error_email(str(e), method_name)
                    raise e
                else:
                    self.log(f"Exception occurred in {method_name}: {str(e)}")
                    i = 0
                    while i < attempts + 1:
                        await self.wait_time()
                        i += 1
                    attempts += 1
        return res

    def to_iterable(self, obj):
        if isinstance(obj, Iterable) and not isinstance(obj, (str, bytes)):
            return obj  # 如果是可迭代的（非字符串或字节），返回原对象
        else:
            return [obj]

if __name__ == "__main__":
    asyncio.run( BaseApi('amazon_ads','LAPASA','US').send_error_email("123","321"))