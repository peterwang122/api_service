import json
import os
import shutil

import yaml
from util.InserOnlineData import ProcessShowData
from util.select_brand import select_brand
from configuration.path import get_config_path
import redis
from config import REDIS_CONFIG

redis_client = redis.Redis(**REDIS_CONFIG)


def find_brand_by_uid(uid,brands):
    # Brand_path = os.path.join(get_config_path(), 'Brand.yml')
    # if os.path.exists(Brand_path):
    #     with open(Brand_path, 'r', encoding='utf-8') as file:
    #         brands = yaml.safe_load(file)
    # else:
    #     # 如果文件不存在，则创建一个新的文件
    #     with open(Brand_path, 'w', encoding='utf-8') as file:
    #         yaml.dump({}, file)  # 创建一个空的 YAML 文件
    #         brands = {}  # 初始化为一个空字典
    if brands is None:
        brands = {}  # 或者根据需要设置其他默认值

    for brand_group, brand_data in brands.items():
        for brand_name, country_data in brand_data.items():
            for country, config in country_data.items():
                # print(f"Checking brand: {brand_name} with UID: {config.get('UID')}")  # 调试输出
                if config.get('UID') == int(uid):
                    return brand_group, brand_name, config

    return None, None, None


def update_brand_info(db, brand_info, new_info):
    # 获取文件路径
    brand_path = os.path.join(get_config_path(), 'Brand.yml')
    temp_brand_path = os.path.join(get_config_path(), 'Brand1.yml')  # 临时文件

    # 读取原文件（如果存在），否则初始化为空字典
    if os.path.exists(brand_path):
        with open(brand_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
    else:
        data = {}  # 如果文件不存在，初始化为空字典

    if data is None:
        data = {}  # 或者根据需要设置其他默认值

    # 更新品牌信息
    if db not in data:
        data[db] = {}

    for brand in brand_info:
        # 更新数据，使用 new_info 的拷贝
        data[db][brand] = {"default": new_info.copy()}

    # 将更新后的数据写入临时文件
    with open(temp_brand_path, 'w', encoding='utf-8') as file:
        yaml.dump(data, file)

    # 只有在写入临时文件成功后，才覆盖原文件
    try:
        os.replace(temp_brand_path, brand_path)  # 使用 os.replace 来覆盖文件
        print(f"Updated {brand_path} with new dbinfo: {new_info}")
    except Exception as e:
        print(f"Failed to replace {brand_path}: {e}")


def update_db_info(db, new_dbinfo, brand_info, db_json):
    try:
        # 获取配置文件路径
        db_info_path = os.path.join(get_config_path(), db_json)

        # 生成临时文件的路径，临时文件命名为 db_json + '.tmp'
        temp_db_info_path = db_info_path + '.tmp'

        # 读取现有的正式 JSON 文件
        if os.path.exists(db_info_path):
            with open(db_info_path, 'r') as f:
                data = json.load(f)
        else:
            data = {}  # 如果正式文件不存在，初始化为空字典

        # 在临时文件中进行更新
        temp_data = data.copy()  # 复制现有数据，修改副本

        # 更新 db 对应的字典
        temp_data[db] = {}

        for brand in brand_info:
            # 更新临时 JSON 数据
            temp_data[db][brand] = {"default": new_dbinfo}

        # 将更新后的数据写入临时文件
        with open(temp_db_info_path, 'w') as temp_file:
            json.dump(temp_data, temp_file, indent=4)

        print(f"Updated temp JSON file with new dbinfo: {new_dbinfo}")

        # 如果临时文件写入没有异常，替换正式文件
        shutil.move(temp_db_info_path, db_info_path)
        print(f"Successfully replaced the original JSON file with updated data.")

    except FileNotFoundError:
        print(f"Error: {db_info_path} not found.")
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from {db_info_path}.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        # 如果出错，可以删除临时文件
        if os.path.exists(temp_db_info_path):
            os.remove(temp_db_info_path)

def get_record_by_id(data, target_id):
    for record in data:
        if record.get('ID') == target_id:
            return record
    return None


# def automatic_configuration():
#     data = {
#         "CloseFlag": 0  # 1 关闭的 0 没有关闭的
#     }
#     data, msg = ProcessShowData.user_account_info(post_data=data)
#     print(data, msg)
#     Brand_path = os.path.join(get_config_path(), 'Brand.yml')
#     if os.path.exists(Brand_path):
#         with open(Brand_path, 'r', encoding='utf-8') as file:
#             brands = yaml.safe_load(file)
#     else:
#         # 如果文件不存在，则创建一个新的文件
#         with open(Brand_path, 'w', encoding='utf-8') as file:
#             yaml.dump({}, file)  # 创建一个空的 YAML 文件
#             brands = {}  # 初始化为一个空字典
#     for item in msg['data']:
#         print(item['ID'])
#         print('-------------------------')
#         db, brand_name, brand_info = find_brand_by_uid(item['ID'],brands)
#         if db and brand_name and brand_info:
#             continue
#         else:
#             if item['DbName'] and item['LogDbName']:
#                 # 分割 DbName 和 LogDbName
#                 db_names = item['DbName'].split(',')
#                 log_db_names = item['LogDbName'].split(',')
#
#                 # 处理 DbName 和 LogDbName
#                 for db_name, log_db_name in zip(db_names, log_db_names):
#                     db_info = db_name.strip()
#                     brand_info = select_brand(db_info)
#                     print(brand_info)
#                     public_value = 0 if db_info in ["amazon_outdoormaster"] else 1
#                     new_info = {
#                         'host': "192.168.5.114",
#                         'user': "root",
#                         'password': "duozhuan888",
#                         'dbname': db_info,
#                         'port': 3308,
#                         'UID': item['ID'],
#                         'public': public_value,
#                         'api_type': "OLD",
#                     }
#                     update_brand_info(db_info,brand_info,new_info)
#                     db_new_info = {
#                         "host": "192.168.2.139",
#                         "user": "wanghequan",
#                         "password": "WHq123123Aa",
#                         "port": 3306,
#                         "db": db_info,
#                         "charset": "utf8mb4",
#                         "use_unicode": True
#                     }
#                     update_db_info(db_info,db_new_info,brand_info,'db_info.json')
#                     log_db_info = log_db_name.strip()
#                     # create_log(log_db_info)
#                     db_log_info = {
#                         "host": "192.168.2.123",
#                         "user": "wanghequan",
#                         "password": "WHq123123Aa",
#                         "port": 3308,
#                         "db": log_db_info,
#                         "charset": "utf8mb4",
#                         "use_unicode": True
#                     }
#                     # Update the JSON file with new dbinfo
#                     update_db_info(db_info,db_log_info,brand_info,'db_info_log.json')
#                     print(f"{item['ID']} done")


# def update_configuration(db):
#     data = {
#         "CloseFlag": 0  # 1 关闭的 0 没有关闭的
#     }
#     data, msg = ProcessShowData.user_account_info(post_data=data)
#
#     # 添加一个标志变量，用于判断是否找到匹配的 db
#     found = False
#
#     for item in msg['data']:
#         if db in item['DbName']:
#             found = True  # 找到匹配的 db
#             print(item['ID'])
#             print('-------------------------')
#             if item['DbName'] and item['LogDbName']:
#                 # 分割 DbName 和 LogDbName
#                 db_names = item['DbName'].split(',')
#                 log_db_names = item['LogDbName'].split(',')
#
#                 # 处理 DbName 和 LogDbName
#                 for db_name, log_db_name in zip(db_names, log_db_names):
#                     db_info = db_name.strip()
#                     brand_info = select_brand(db_info)
#                     print(brand_info)
#                     public_value = 0 if db_info in ["amazon_outdoormaster"] else 1
#                     new_info = {
#                         'host': "192.168.5.114",
#                         'user': "root",
#                         'password': "duozhuan888",
#                         'dbname': db_info,
#                         'port': 3308,
#                         'UID': item['ID'],
#                         'public': public_value,
#                         'api_type': "OLD",
#                     }
#                     update_brand_info(db_info, brand_info, new_info)
#                     db_new_info = {
#                         "host": "192.168.2.139",
#                         "user": "wanghequan",
#                         "password": "WHq123123Aa",
#                         "port": 3306,
#                         "db": db_info,
#                         "charset": "utf8mb4",
#                         "use_unicode": True
#                     }
#                     update_db_info(db_info, db_new_info, brand_info, 'db_info.json')
#                     log_db_info = log_db_name.strip()
#                     # create_log(log_db_info)
#                     db_log_info = {
#                         "host": "192.168.2.123",
#                         "user": "wanghequan",
#                         "password": "WHq123123Aa",
#                         "port": 3308,
#                         "db": log_db_info,
#                         "charset": "utf8mb4",
#                         "use_unicode": True
#                     }
#                     # Update the JSON file with new dbinfo
#                     update_db_info(db_info, db_log_info, brand_info, 'db_info_log.json')
#                     print(f"{item['ID']} done")
#             break
#     # 如果循环结束后没有找到匹配的 db，抛出异常
#     if not found:
#         raise ValueError(f"{db} 该数据库不存在")

def automatic_configuration():
    redis_client.flushdb()
    print("Redis 缓存已清除")
    data = {
        "CloseFlag": 0  # 1 关闭的 0 没有关闭的
    }
    data, msg = ProcessShowData.user_account_info(post_data=data)
    for item in msg['data']:
        print(item['ID'])
        print('-------------------------')
        if item['DbName'] and item['LogDbName']:
            # 分割 DbName 和 LogDbName
            db_names = item['DbName'].split(',')
            log_db_names = item['LogDbName'].split(',')

            # 处理 DbName 和 LogDbName
            for db_name, log_db_name in zip(db_names, log_db_names):
                db_info = db_name.strip()
                cache_brand_key = f"brand_info:{db_info}"
                brand_info = {
                    'UID': item['ID'],
                    "db": db_info,
                    "is_new": item['IsDistributor'],
                }
                redis_client.set(cache_brand_key, json.dumps(brand_info))
                print(f"缓存写入成功: {cache_brand_key}")

                # 使用传入的 db 作为缓存键
                cache_key = f"db_info:{db_info}"
                db_info_data = {
                    "host": "192.168.2.139",
                    "user": "wanghequan",
                    "password": "WHq123123Aa",
                    "port": 3306,
                    "db": db_info,
                    "charset": "utf8mb4",
                    "use_unicode": True
                }
                redis_client.set(cache_key, json.dumps(db_info_data))
                print(f"缓存写入成功: {cache_key}")

                log_db_info = log_db_name.strip()
                db_log_info = {
                    "host": "192.168.2.123",
                    "user": "wanghequan",
                    "password": "WHq123123Aa",
                    "port": 3308,
                    "db": log_db_info,
                    "charset": "utf8mb4",
                    "use_unicode": True
                }
                # Update the JSON file with new dbinfo
                cache_log_key = f"db_info_log:{db_info}"
                redis_client.set(cache_log_key, json.dumps(db_log_info))
                print(f"缓存写入成功: {cache_log_key}")


def update_configuration(db):
    data = {
        "CloseFlag": 0  # 1 关闭的 0 没有关闭的
    }
    data, msg = ProcessShowData.user_account_info(post_data=data)

    # 添加一个标志变量，用于判断是否找到匹配的 db
    found = False

    for item in msg['data']:
        if db in item['DbName']:
            found = True  # 找到匹配的 db
            print(item['ID'])
            print('-------------------------')
            if item['DbName'] and item['LogDbName']:
                # 分割 DbName 和 LogDbName
                db_names = item['DbName'].split(',')
                log_db_names = item['LogDbName'].split(',')

                # 处理 DbName 和 LogDbName
                for db_name, log_db_name in zip(db_names, log_db_names):
                    db_info = db_name.strip()
                    cache_brand_key = f"brand_info:{db_info}"
                    brand_info = {
                        'UID': item['ID'],
                        "db": db_info,
                        "is_new": item['IsDistributor'],
                    }
                    redis_client.set(cache_brand_key, json.dumps(brand_info))
                    print(f"缓存写入成功: {cache_brand_key}")

                    # 使用传入的 db 作为缓存键
                    cache_key = f"db_info:{db_info}"
                    db_info_data = {
                        "host": "192.168.2.139",
                        "user": "wanghequan",
                        "password": "WHq123123Aa",
                        "port": 3306,
                        "db": db_info,
                        "charset": "utf8mb4",
                        "use_unicode": True
                    }
                    redis_client.set(cache_key, json.dumps(db_info_data))
                    print(f"缓存写入成功: {cache_key}")

                    log_db_info = log_db_name.strip()
                    db_log_info = {
                        "host": "192.168.2.123",
                        "user": "wanghequan",
                        "password": "WHq123123Aa",
                        "port": 3308,
                        "db": log_db_info,
                        "charset": "utf8mb4",
                        "use_unicode": True
                    }
                    # Update the JSON file with new dbinfo
                    cache_log_key = f"db_info_log:{db_info}"
                    redis_client.set(cache_log_key, json.dumps(db_log_info))
                    print(f"缓存写入成功: {cache_log_key}")
            break
    # 如果循环结束后没有找到匹配的 db，抛出异常
    if not found:
        raise ValueError(f"{db} 该数据库不存在")
if __name__ == '__main__':
    # automatic_configuration()
    # res = find_brand_by_uid(1)
    # update_configuration("amazon_outdoormaster")
    # print(res)
    data = {
        "CloseFlag": 0  # 1 关闭的 0 没有关闭的
    }
    data, msg = ProcessShowData.user_account_info(post_data=data)
    print(data, msg)