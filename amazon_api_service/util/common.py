import asyncio
import json
import time
import traceback
import pytz
import os
import yaml
from datetime import datetime, timedelta
from db.tools_db_sp import DbSpTools
from util.InserOnlineData import ProcessShowData
from util.automatic_configuration import automatic_configuration,update_configuration
from logs.logger import logger
import redis
from config import REDIS_CONFIG, CONFIG, CREDENTIALS,COUNTRY_REGION_MAPPING

redis_client = redis.Redis(**REDIS_CONFIG)

async def get_profile_id_info(db, market, brand):
    try:
        api = DbSpTools(db,brand,market)
        profileId, region = await api.get_profileId(market)
        return profileId,region
    except Exception as e:
        logger.error(f"Error retrieving profile IDs from database: {e}")
        return None,None


def new_get_api_config(uid, region, api_type, is_new=False):
    try:
        if not is_new:
            print("old api 标识")
            config = CONFIG['OLD']
        else:
            print("new api 标识")
            config = CONFIG["NEW"]

        if config[api_type]:
            api_config = {}
            print("不存在 UID token 数据")
            data = {
                "UID": uid,  # 所属用户
                "AreaCode": region,  # 那个地区
                "OuthType": api_type  # 操作类型
            }
            res, data = ProcessShowData.get_accesstoken(data)
            logger.info(f"res: {res}, data: {data}")
            if res:
                result = {
                    "client_id": config[api_type]['client_id'],
                    "client_secret": config[api_type]['client_secret'],
                    "refresh_token": data['data']['refresh_token'],
                    "access_token": data['data']['access_token']
                }
                expires_in = int(data['data']['expires_timestamp']) - int(time.time())
            else:
                result = {}
                expires_in = 0
            return result, expires_in
        else:
            return {}, 0
    except Exception as e:
        logger.error(f"Error retrieving client IDs from database: {e}")
        return {}, 0



# 获取 ad my_credentials
async def get_ad_my_credentials(db, market, brand):
    cache_key = f"brand_info:{db}"
    # 尝试从 Redis 缓存中获取数据
    cached_data = redis_client.get(cache_key)
    if cached_data:
        brand_info = json.loads(cached_data)
    else:
        update_configuration(db)
        cached_data = redis_client.get(cache_key)
        brand_info = json.loads(cached_data)
    is_new = brand_info['is_new']
    UID = brand_info['UID']
    region = COUNTRY_REGION_MAPPING.get(market, None)

    # 最大重试次数
    MAX_RETRIES = 3
    retry_count = 0
    api_config = {}
    # 重试机制
    while retry_count < MAX_RETRIES:
        api_config, expires_in = new_get_api_config(UID, region, "AD",is_new)
        if api_config:  # 如果获取到有效的配置，退出重试循环
            break
        else:
            retry_count += 1
            logger.error(f"No API config found for region: {region}. Retrying ({retry_count}/{MAX_RETRIES})...")
            time.sleep(10)
    profileid, region = await get_profile_id_info(db, market, brand)
    my_credentials = dict(
        refresh_token=api_config['refresh_token'],
        client_id=api_config['client_id'],
        client_secret=api_config['client_secret'],
        profile_id=str(profileid),
    )
    # print("api_config==", api_config)
    return my_credentials, api_config['access_token'], expires_in