import asyncio
import multiprocessing
import os
from decimal import Decimal
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import aiohttp
import pandas as pd
import pymysql
import requests
import random
import pyppeteer
from lxml import html
import json
import csv
import time
import redis
from config import REDIS_CONFIG
from db.tools_db_new_sp import DbNewSpTools
from db.tools_db_sp import DbSpTools

redis_client = redis.Redis(db=12,**REDIS_CONFIG)

def get_proxies(region):
    proxies = "http://192.168.2.165:7890"
    if region in ("JP","US"):
        print("有代理")
        return proxies
    else:
        return None

def make_url(market,asin):
    urls = generate_urls(market)
    return f'{urls}dp/{asin}'

async def fetch_last_category(market,asin, max_retries=100, delay=2):
    url = make_url(market,asin)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    async with aiohttp.ClientSession() as session:
        for attempt in range(max_retries):
            try:
                # 发送异步请求
                async with session.get(url, headers=headers, proxy=get_proxies(market)) as response:
                    # 检查请求是否成功
                    if response.status == 200:
                        # 读取响应内容
                        content = await response.text()

                        # 解析HTML内容
                        soup = BeautifulSoup(content, 'html.parser')

                        # 查找面包屑导航部分
                        breadcrumb = soup.find('div', {'id': 'wayfinding-breadcrumbs_container'})

                        if breadcrumb:
                            categories = breadcrumb.find_all('a', {'class': 'a-link-normal'})

                            if categories:
                                # 获取最后一个分类
                                last_category = categories[-1].get_text(strip=True)
                                return last_category
                            else:
                                print('No categories found')
                        else:
                            print('Breadcrumb not found')
                    else:
                        print(f'Failed to retrieve the page. Status code: {response.status}')
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                print(f'Attempt {attempt + 1} failed: {e}')
                if attempt < max_retries - 1:
                    await asyncio.sleep(delay)  # 等待一段时间后重试
                else:
                    print('Max retries reached. Giving up.')
                    return None

    return None
def generate_urls(market):
    # URL 模板
    url_templates = {
    "UK": "https://www.amazon.co.uk/",
    "US": "https://www.amazon.com/",
    "DE": "https://www.amazon.de/",
    "FR": "https://www.amazon.fr/",
    "IT": "https://www.amazon.it/",
    "ES": "https://www.amazon.es/",
    "JP": "https://www.amazon.co.jp/",
    "AU": "https://www.amazon.com.au/",
    "CA": "https://www.amazon.ca/",
    "MX": "https://www.amazon.com.mx/",
    "AE": "https://www.amazon.ae/"
}
    base_url = url_templates.get(market.upper())
    if not base_url:
        print(f"不支持该国家的 Amazon 网站：{market}")
        raise f"不支持该国家的 Amazon 网站：{market}"
    return base_url


async def pachong(db, brand, market, search_term):
    waiting_count = 0
    MAX_WAITING_COUNT = 10
    urls = generate_urls(market)
    all_asin_data = []

    # 处理搜索词，若有空格则替换为 "+"
    search_term = search_term.replace(" ", "+")
    cache_key = f"pachong:{market}:{search_term}"  # Redis 缓存键

    # 尝试从 Redis 缓存中获取数据
    cached_data = redis_client.get(cache_key)
    if cached_data:
        print(f"已缓存 {market} - {search_term} 的 ASIN，跳过爬取")
        return json.loads(cached_data)

    async def extract_asin_data(url):
        while True:
            try:
                print(url)
                # 设置代理和其他启动选项
                browser = await pyppeteer.launch({
                    'headless': True,  # 启动无头浏览器
                    'args': [
                        '--no-sandbox',
                        '--disable-setuid-sandbox',
                        '--proxy-server=http://192.168.2.165:7890'  # 设置代理
                    ]
                })

                # 创建新页面
                page = await browser.newPage()
                # 访问目标网址
                await page.goto(url)
                # 获取页面内容
                asins = await page.evaluate('''() => {
                            const asins = [];
                            const elements = document.querySelectorAll('[data-asin]');
                            elements.forEach(el => {
                                if (el.hasAttribute('data-asin')) {
                                    asins.push(el.getAttribute('data-asin'));
                                }
                            });
                            return asins;
                        }''')
                asin_list = []
                # 关闭浏览器
                await browser.close()
                print(asins)
                for element in asins:
                    if element and element.startswith('B0'):
                        asin_list.append(element)
                print(asin_list)
                if len(asins) > 2:
                    return asin_list
                else:
                    await asyncio.sleep(random.uniform(3, 5))  # 如果请求失败，等待5秒后重试
                    return None
            except requests.exceptions.RequestException as e:
                # 捕获所有请求相关的异常
                print(f"请求失败，错误信息：{e}")
                await asyncio.sleep(random.uniform(3, 5))  # 等待5秒后重试
                return None
            finally:
                await browser.close()

    for page_num in range(1, 8):
        await asyncio.sleep(random.uniform(3, 5))
        consecutive_empty_count = 0
        url = f"{urls}s?k={search_term}&page={page_num}&ref=sr_pg_{page_num}"
        print(f"正在处理 {market} - {search_term} 的第 {page_num} 页...")
        asin_data = None

        while asin_data is None:
            asin_data = []  # 清空之前的数据
            try:
                asin_data = await extract_asin_data(url)
            except Exception as e:
                print(f"爬取失败，错误：{e}")

            if asin_data is None:
                consecutive_empty_count += 1
                print(f"连续返回空数据 {consecutive_empty_count} 次")

                if consecutive_empty_count >= 3:
                    print("连续3次返回空数据，等待60分钟后继续...")
                    waiting_count += 1

                    if waiting_count >= MAX_WAITING_COUNT:
                        print(f"已达到最大等待次数 {MAX_WAITING_COUNT}，停止所有任务...")
                        raise print("Reached max wait count, cancelling all tasks.")
                    current_time = datetime.now()
                    # 打印当前时间（默认格式：年-月-日 时:分:秒.毫秒）
                    print(current_time)
                    await asyncio.sleep(60 * 60)  # 等待10分钟
                    consecutive_empty_count = 0  # 重置计数器
                else:
                    print(f"当前数据量 0，重新获取数据...")
            else:
                break

        # 记录第一页的数据量，后续页面将根据此值来判断
        if page_num == 1:
            first_page_data_count = min(len(asin_data), 48)

        # 将当前页的数据添加到总数据列表
        all_asin_data.extend(asin_data)

        # 后续页面根据第一页的抓取量来判断是否继续抓取
        if first_page_data_count is not None and len(asin_data) < first_page_data_count:
            print(f"第 {page_num} 页抓取的数据小于第一页的数据量，停止抓取后续页...")
            break  # 停止抓取后续页面

    # 将数据存入 Redis 缓存，设置过期时间为 12 小时
    redis_client.set(cache_key, json.dumps(all_asin_data), ex=60 * 60 * 12)
    print(f"all_asin_data:{all_asin_data}")
    return all_asin_data


async def searchterm_asin(db,brand,market,day,order,num):
    api = DbSpTools(db, brand, market)
    info = await api.campaign_info(num)
    if not info:
        print(f"品牌 {brand} 国家 {market} 没有找到有效的 campaignId 数据。")
        return [f"品牌{brand} 国家{market} 没有有效的 campaignId 数据。"]
    sql_results = await api.get_classification_title(market)
    print(sql_results)
    asin_cache = {}
    valid_campaign_data = {campaign['campaignId']: campaign['calculated_value'] for campaign in info}
    if sql_results is not None and not sql_results.empty:
        result = sql_results.groupby(['parent_asins'])[
            ['classification_rank_title','campaignId']].agg(list)
        massage = []
        # 循环处理每一行数据
        for parent_asin, series in result.iterrows():
            print(f"父ASIN：{parent_asin}")
            classification_rank_titles = series['classification_rank_title']
            campaignIds = series['campaignId']
            # 查找是否有一个 campaignId 在 valid_campaign_data 中
            valid_values = [valid_campaign_data[campaignId] for campaignId in campaignIds if
                            campaignId in valid_campaign_data]

            # 如果有有效的 campaignId，则取出最大值
            if valid_values:
                calculated_value = max(valid_values)
            else:
                print(f"父ASIN{parent_asin}无需要添加的campaignId，跳过")
                continue  # 没有找到有效的 campaignId，则跳过
            all_asin_data = []
            seen_asins = set()
            if classification_rank_titles or classification_rank_titles == '':
                print("test:",classification_rank_titles)
                for i in classification_rank_titles:
                    if i:
                        title = i

                        asin_data = await pachong(db, brand, market, title)
                        for asin in asin_data:
                            if asin not in seen_asins:
                                all_asin_data.append(asin)  # 添加到最终的列表
                                seen_asins.add(asin)  # 将该 ASIN 标记为已处理
                        if len(all_asin_data) >= int(calculated_value):
                            print("已收集到 400 条 ASIN 数据，停止添加。")
                            break
            if len(all_asin_data) < int(calculated_value):
                sercahterms = await api.get_serachterm(market,parent_asin,day,order)
                for sercahterm in sercahterms:
                    if sercahterm:

                        asin_data1 = await pachong(db, brand, market, sercahterm)
                        for asin in asin_data1:
                            if asin not in seen_asins:
                                all_asin_data.append(asin)  # 添加到最终的列表
                                seen_asins.add(asin)  # 将该 ASIN 标记为已处理
                        if len(all_asin_data) >= int(calculated_value):
                            print("已收集到 400 条 ASIN 数据，停止添加。")
                            break
                    if len(all_asin_data) >= int(calculated_value):
                        print("已收集到 400 条 ASIN 数据，停止添加。")
                        break  # 如果外层循环也达到了 1000 条，直接跳出
            if len(all_asin_data) == 0:
                sercahterm = await fetch_last_category(market,parent_asin)
                if sercahterm:
                    asin_data1 = await pachong(db, brand, market, sercahterm)
                    for asin in asin_data1:
                        if asin not in seen_asins:
                            all_asin_data.append(asin)  # 添加到最终的列表
                            seen_asins.add(asin)  # 将该 ASIN 标记为已处理
            print(all_asin_data)
            updates = []
            today = datetime.today()
            cur_time = today.strftime('%Y-%m-%d')
            for asin in all_asin_data:
                try:
                    updates.append({
                        'market': market,
                        'classification_id': parent_asin,
                        'Asin': asin,
                        'Rank': 0,
                        'Date': cur_time
                    })
                except json.JSONDecodeError:
                    print("JSON 解码错误")
            api1 = DbNewSpTools(db, brand, market)
            await api1.init()
            await api1.batch_expanded_asin_info(updates)
            info = f"已抓取父ASIN：{parent_asin}的搜索词竞品ASIN共{len(all_asin_data)}个"
            massage.append(info)
        print(massage)
        return massage
    else:
        return [f"品牌{brand} 国家{market}托管ASIN无小分类，无搜索词竞品ASIN"]


if __name__ == "__main__":
    asyncio.run(searchterm_asin('amazon_68_LILLEPRINS','LILLEPRINS','US',60,1,1000))

