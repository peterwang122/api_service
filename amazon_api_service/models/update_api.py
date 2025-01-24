from datetime import datetime

from method.sp_api import auto_api_sp
from method.sd_api import auto_api_sd


async def update_api(data):
    if data['type'] == 'SP':
        code,e = await sp_api(data)
    elif data['type'] == 'SD':
        code,e = await sd_api(data)
    return code,e

async def sp_api(data):
    current_time = datetime.now()
    # 打印当前时间（默认格式：年-月-日 时:分:秒.毫秒）
    print('方法前：',current_time)
    api = auto_api_sp(data['brand'],data['market'],data['db'],data['user'])
    if data['require'] == 'bid':
        if data['position'] == 'campaign':
            code,e = await api.update_sp_ad_budget(data['ID'], data['text'])
        elif data['position'] == 'placement':
            code,e = await api.update_sp_ad_placement(data['ID'], data['text'], data['placement'])
        elif data['position'] == 'keyword':
            code,e = await api.update_sp_ad_keyword(data['ID'], data['text'])
        elif data['position'] == 'product_target':
            code,e = await api.update_sp_ad_product_targets(data['ID'], data['text'])
        elif data['position'] == 'automatic_targeting':
            code,e = await api.update_sp_ad_automatic_targeting(data['ID'], data['text'])
    elif data['require'] == 'bid_batch':
        if data['position'] == 'keyword':
            code,e = await api.update_sp_ad_keyword_batch(data['ID'], data['text'])
        elif data['position'] == 'campaign':
            code,e = await api.update_sp_ad_budget_batch(data['ID'], data['text'])
        elif data['position'] == 'product_target':
            code,e = await api.update_sp_ad_automatic_targeting_batch(data['ID'], data['text'])
        elif data['position'] == 'automatic_targeting':
            code,e = await api.update_sp_ad_automatic_targeting_batch(data['ID'], data['text'])
    elif data['require'] == 'state':
        if data['position'] == 'campaign':
            code,e = await api.auto_campaign_status(data['ID'], data['text'])
        elif data['position'] == 'adgroup':
            code,e = await api.auto_adgroup_status(data['ID'], data['text'])
        elif data['position'] == 'sku':
            code,e = await api.auto_sku_status(data['ID'], data['text'])
        elif data['position'] == 'sku_task':
            code, e = await api.auto_sku_status_task(data['ID'], data['text'], data['campaignId'], data['campaignName'], data['click'], data['cpc'], data['acos'])
        elif data['position'] == 'keyword':
            code,e = await api.auto_keyword_status(data['ID'], data['text'])
        elif data['position'] == 'product_target':
            code,e = await api.auto_targeting_status(data['ID'], data['text'])
        elif data['position'] == 'automatic_targeting':
            code,e = await api.auto_targeting_status(data['ID'], data['text'])
    elif data['require'] == 'state_batch':
        if data['position'] == 'keyword':
            code,e = await api.auto_keyword_status_batch(data['ID'], data['text'])
        elif data['position'] == 'product_target':
            code,e = await api.auto_targeting_status_batch(data['ID'], data['text'])
        elif data['position'] == 'sku_task':
            code,e = await api.auto_sku_status_task_batch(data['ID'], data['text'], data['campaignId'], data['campaignName'], data['click'], data['cpc'], data['acos'])
    elif data['require'] == 'create':
        if data['position'] == 'product_target':
            code,e = await api.create_product_target(data['ID'], data['text'], data['campaignId'], data['adGroupId'])
        elif data['position'] == 'category':
            code,e = await api.create_category(data['ID'], data['text'], data['campaignId'], data['adGroupId'])
        elif data['position'] == 'product_target_asin':
            code,e = await api.create_product_target_asin(data['ID'], data['text'], data['campaignId'], data['adGroupId'])
        elif data['position'] == 'product_target_asin_expended':
            code,e = await api.create_product_target_asin_expended(data['ID'], data['text'], data['campaignId'], data['adGroupId'])
        elif data['position'] == 'keyword':
            code,e = await api.create_keyword(data['ID'], data['text'], data['campaignId'], data['adGroupId'], data['matchType'])
        elif data['position'] == 'negative_target':
            code,e = await api.create_negative_target(data['ID'], data['campaignId'], data['adGroupId'], data['matchType'])
        elif data['position'] == 'campaign':
            code,e = await api.create_campaign(data['ID'], data['text'], data['matchType'])
    elif data['require'] == 'create_batch':
        if data['position'] == 'negative_target':
            code,e = await api.create_negative_target_batch(data['ID'], data['campaignId'], data['adGroupId'], data['matchType'], data['campaignName'], data['click'], data['cpc'], data['acos'])
        elif data['position'] == 'keyword':
            code,e = await api.create_keyword_batch(data['ID'], data['text'], data['campaignId'], data['adGroupId'], data['matchType'])
        elif data['position'] == 'product_target':
            code,e = await api.create_product_target_batch(data['ID'], data['text'], data['campaignId'], data['adGroupId'], data['matchType'])
    elif data['require'] == 'name':
        if data['position'] == 'campaign':
            code,e = await api.auto_campaign_name(data['ID'], data['text'])
    elif data['require'] == 'delete':
        if data['position'] == 'negative_target':
            code,e = await api.delete_negative_target(data['ID'])
        elif data['position'] == 'negative_keyword':
            code,e = await api.delete_negative_keyword(data['ID'])
        elif data['position'] == 'keyword':
            code,e = await api.delete_keyword(data['ID'])
        elif data['position'] == 'product_target':
            code,e = await api.delete_product_target(data['ID'])
        elif data['position'] == 'sku':
            code,e = await api.delete_sku(data['ID'])
    return code,e

async def sd_api(data):
    api = auto_api_sd(data['brand'],data['market'],data['db'],data['user'])
    if data['require'] == 'bid':
        if data['position'] == 'campaign':
            code,e = await api.update_sd_ad_budget(data['ID'], data['text'])
        elif data['position'] == 'product_target':
            code,e = await api.update_sd_ad_product_targets(data['ID'], data['text'])
    elif data['require'] == 'state':
        if data['position'] == 'campaign':
            code,e = await api.auto_campaign_status(data['ID'], data['text'])
        elif data['position'] == 'sku':
            code,e = await api.auto_sku_status(data['ID'], data['text'])
        elif data['position'] == 'product_target':
            code,e = await api.auto_targeting_status(data['ID'], data['text'])
    elif data['require'] == 'create':
        if data['position'] == 'product_target':
            code,e = await api.create_product_target(data['ID'], data['text'], data['campaignId'], data['adGroupId'])
        elif data['position'] == 'product_target_new':
            code,e = await api.create_product_target_new(data['ID'], data['text'], data['campaignId'], data['adGroupId'])
        elif data['position'] == 'product_target_asin':
            code,e = await api.create_product_target_asin(data['ID'], data['text'], data['adGroupId'])
    elif data['require'] == 'name':
        if data['position'] == 'campaign':
            code,e = await api.auto_campaign_name(data['ID'], data['text'])
    return code,e
