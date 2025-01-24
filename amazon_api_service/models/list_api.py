from method.sp_api import auto_api_sp

async def list_api(data):
    if data['type'] == 'SP':
        code, info, e = await sp_api(data)
    # elif data['type'] == 'SD':
    #     code = sd_api(data)
    return code, info, e

async def sp_api(data):
    api = auto_api_sp(data['brand'],data['market'],data['db'],data['user'])
    if data['require'] == 'list':
        if data['position'] == 'TargetingClause':
            code,info,e = await api.list_adGroup_TargetingClause(data['text'])
        elif data['position'] == 'product':
            code,info,e = await api.get_product_api(data['text'])
        elif data['position'] == 'Targetingrecommendations':
            code,info,e = await api.list_adGroup_Targetingrecommendations(data['text'])
        elif data['position'] == 'refinements':
            code,info,e = await api.list_category_refinements(data['text'])
        elif data['position'] == 'CampaignNegativeKeywords':
            code,info,e = await api.list_CampaignNegativeKeywords(data['text'])
    return code, info, e