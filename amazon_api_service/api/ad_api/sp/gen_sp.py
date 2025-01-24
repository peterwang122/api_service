import asyncio
from datetime import datetime
from api.ad_api.sp.tools_sp import ToolsSP
from db.tools_db_new_sp import DbNewSpTools


class GenSP(ToolsSP):
    def __init__(self, db, brand, market):
        super().__init__(db, brand, market)

    async def create_camapign(self,name,startDate,dynamicBidding,portfolioId,endDate,targetingType,state,budgetType,budget,user='test'):
        campaigninfo = {
          "campaigns": [
            {
              "portfolioId": portfolioId,
              "endDate": endDate,
              "name": name,
              "targetingType": targetingType,
              "state": state,
              "dynamicBidding": dynamicBidding,
              "startDate": startDate,
              "budget": {
                "budgetType": budgetType,
                "budget": budget
              }
            }
          ]
        }
        # 执行创建
        res = await self.create_campaigns_api(campaigninfo)

        if isinstance(res, dict) and res['campaigns']['success']:
            status = "success"
            campaign_id = res['campaigns']['success'][0]['campaignId']
            error_message = None
        else:
            status = "failed"
            campaign_id = None
            error_message = res['campaigns']['error'][0]['errors'][0]['errorType'] if isinstance(res, dict) else res
        # 根据创建结果更新log
        dbNewTools = DbNewSpTools(self.db, self.brand,self.market)
        # 异步初始化
        await dbNewTools.init()
        await dbNewTools.create_sp_campaigin(
            self.market,
            portfolioId,
            endDate,
            name,
            campaign_id,
            targetingType,
            state,
            startDate,
            budgetType,
            budget,
            status,
            datetime.now(),
            "SP",
            error_message,
            user
        )
        return campaign_id, error_message

    async def update_camapign_v0(self,campaignId,campaignName,budget_old,budget_new,state, user='test'):
        campaign_info = {
            "campaigns": [
                {
                    "campaignId": str(campaignId),
                    "state": state,
                    "budget": {
                        "budgetType": "DAILY",
                        "budget": budget_new
                    }
                }
            ]
        }
        #调用api
        res = await self.update_campaigns(campaign_info)

        if isinstance(res, dict) and res['campaigns']['success']:
            status = "success"
            campaign_id = res['campaigns']['success'][0]['campaignId']
            error_message = None
        else:
            status = "failed"
            campaign_id = None
            error_message = res['campaigns']['error'][0]['errors'][0]['errorType'] if isinstance(res, dict) else res
        newdbtool = DbNewSpTools(self.db, self.brand,self.market)
        await newdbtool.init()
        await newdbtool.update_sp_campaign(
            self.market,
            campaignName,
            campaignId,
            'budget',
            budget_old,
            budget_new,
            None,
            None,
            error_message,
            status,
            datetime.now(),
            user)
        return error_message

    async def update_camapign_batch(self,info, user='test'):
        campaign_info = {
            "campaigns": []
        }
        for item in info:
            campaign_info["campaigns"].append({
                    "campaignId": str(item['campaignId']),
                    "state": item['state'],
                    "budget": {
                        "budgetType": "DAILY",
                        "budget": item['bid_new']
                    }
                }
            )
        # 修改关键词操作
        res = await self.update_campaigns(campaign_info)
        # 存储更新记录到数据库
        dbNewTools = DbNewSpTools(self.db, self.brand, self.market)
        await dbNewTools.init()
        # 获取成功的 index
        success_indices = {item['index']: item['campaignId'] for item in res['campaigns']['success']}
        updates = []
        for idx, item in enumerate(info):
            # 检查当前的索引是否在成功的索引中
            if idx in success_indices:
                targeting_state = "success"
                campaignId = success_indices[idx]
            else:
                targeting_state = "failed"
                campaignId = None  # 或者设置为其他默认值

            updates.append({
                'market': self.market,
                'campaign_name': item['campaign_name'],
                'campaign_id': item['campaignId'],
                'change_type': 'budget',  # Assuming you have this value in `info`
                'budget_old': item['bid'],
                'budget_new': item['bid_new'],
                'standards_acos': None,
                'acos': None,
                'beizhu': None,
                'status': targeting_state,
                'update_time': datetime.now(),
                'user': user
            })
        # 批量插入到数据库
        await dbNewTools.batch_update_sp_campaign(updates)

    async def update_camapign_name(self,campaignId,campaignName,campaignName_new, user='test'):
        campaign_info = {
            "campaigns": [
                {
                    "campaignId": str(campaignId),
                    "name": campaignName_new
                }
            ]
        }
        #调用api
        res = await self.update_campaigns(campaign_info)

        if isinstance(res, dict) and res['campaigns']['success']:
            status = "success"
            campaign_id = res['campaigns']['success'][0]['campaignId']
            error_message = None
        else:
            status = "failed"
            campaign_id = None
            error_message = res['campaigns']['error'][0]['errors'][0]['errorType'] if isinstance(res, dict) else res
        newdbtool = DbNewSpTools(self.db, self.brand,self.market)
        await newdbtool.init()
        await newdbtool.update_sp_campaign(self.market, campaignName, campaignId,'campaignName',campaignName,campaignName_new,None,None,error_message,status,datetime.now(), user)
        return error_message

    async def update_camapign_status(self,campaignId,campaignName,state,state_new, user='test'):
        campaign_info = {
            "campaigns": [
                {
                    "campaignId": str(campaignId),
                    "state": state_new
                }
            ]
        }
        #调用api
        res = await self.update_campaigns(campaign_info)

        if isinstance(res, dict) and res['campaigns']['success']:
            status = "success"
            campaign_id = res['campaigns']['success'][0]['campaignId']
            error_message = None
        else:
            status = "failed"
            campaign_id = None
            error_message = res['campaigns']['error'][0]['errors'][0]['errorType'] if isinstance(res, dict) else res
        newdbtool = DbNewSpTools(self.db, self.brand,self.market)
        await newdbtool.init()
        await newdbtool.update_sp_campaign(self.market, campaignName, campaignId,'campaignStatus',state,state_new,None,None,error_message,status,datetime.now(), user)
        return error_message

    async def update_campaign_placement(self,campaignId,Budget,percentage,placement, user='test'):
        campaign_placement_info = {
            "campaigns": [
                {
                    "campaignId": campaignId,
                    "dynamicBidding": {
                        "placementBidding": [
                            {
                                "percentage": percentage,
                                "placement": placement
                            },
                        ],
                    },
                }
            ]
        }

        # api更新
        res = await self.update_campaigns(campaign_placement_info)

        if isinstance(res, dict) and res['campaigns']['success']:
            status = "success"
            campaign_id = res['campaigns']['success'][0]['campaignId']
            error_message = None
        else:
            status = "failed"
            campaign_id = None
            error_message = res['campaigns']['error'][0]['errors'][0]['errorType'] if isinstance(res, dict) else res
        # 根据结果写入日志
        #     def update_sp_campaign_placement(self,market,campaignId,p_top,p_top_percentage,p_res_of_search,p_res_of_search_percentage,p_product_page,p_product_page_percentage,status,update_time):
        newdbtool = DbNewSpTools(self.db, self.brand,self.market)
        await newdbtool.init()
        await newdbtool.update_sp_campaign_placement(self.market,campaignId,placement,Budget,percentage,error_message,status,datetime.now(), user)
        return error_message

    async def create_adgroup(self,campaignId,name,defaultBid,state,user='test'):
        adgroup_info = {
            "adGroups": [
                {
                    "campaignId": campaignId,
                    "name": name,
                    "state": state,
                    "defaultBid": defaultBid
                }
            ]
        }
        res = await self.create_adGroup_api(adgroup_info)

        if isinstance(res, dict) and res['adGroups']['success']:
            status = "success"
            adGroupId = res['adGroups']['success'][0]['adGroupId']
            error_message = None
        else:
            status = "failed"
            adGroupId = None
            error_message = res['adGroups']['error'][0]['errors'][0]['errorType'] if isinstance(res, dict) else res
        # 根据结果更新log
        #     def create_sp_adgroups(self,market,campaignId,adGroupName,adGroupId,state,defaultBid,adGroupState,update_time):
        dbNewTools = DbNewSpTools(self.db, self.brand,self.market)
        await dbNewTools.init()
        await dbNewTools.create_sp_adgroups(self.market,campaignId,name,adGroupId,state,defaultBid,error_message,status,datetime.now(),None,"SP",user)
        return adGroupId,error_message

    async def update_adgroup(self,adGroupName,adGroupId,state,state_new,user='test'):
        adgroup_info = {
            "adGroups": [
                {
                    "name": adGroupName,
                    "state": state_new,
                    "adGroupId": adGroupId
                }
            ]
        }
        res = await self.update_adGroup_api(adgroup_info)

        if isinstance(res, dict) and res['adGroups']['success']:
            status = "success"
            adGroupId = res['adGroups']['success'][0]['adGroupId']
            error_message = None
        else:
            status = "failed"
            adGroupId = None
            error_message = res['adGroups']['error'][0]['errors'][0]['errorType'] if isinstance(res, dict) else res
        # 根据结果更新log
        #     def create_sp_adgroups(self,market,campaignId,adGroupName,adGroupId,state,defaultBid,adGroupState,update_time):
        dbNewTools = DbNewSpTools(self.db, self.brand,self.market)
        await dbNewTools.init()
        await dbNewTools.update_sp_adgroups(self.market,adGroupName,adGroupId,None,0,None,None,state_new,status,datetime.now(),user)
        return error_message

    async def add_adGroup_negative_keyword_v0(self,campaignId,adGroupId,keywordText,matchType,state, user = 'test'):

        adGroup_negative_keyword_info = {
          "negativeKeywords": [
            {
              "campaignId": str(campaignId),
              "matchType": matchType,
              "state": state,
              "adGroupId": str(adGroupId),
              "keywordText": keywordText
            }
          ]
        }
        # api更新
        res = await self.add_adGroup_negativekw(adGroup_negative_keyword_info)

        if isinstance(res, dict) and res['negativeKeywords']['success']:
            status = "success"
            negativeKeywordId = res['negativeKeywords']['success'][0]['negativeKeywordId']
            error_message = None
        else:
            status = "failed"
            negativeKeywordId = None
            error_message = res['negativeKeywords']['error'][0]['errors'][0]['errorType'] if isinstance(res, dict) else res
        # 结果写入日志
        #  def add_sp_adGroup_negativeKeyword(self, market, adGroupName, adGroupId, campaignId, campaignName, matchType,
        #                                         keyword_state, keywordText, campaignNegativeKeywordId, operation_state,
        #                                         update_time):
        newdbtool = DbNewSpTools(self.db, self.brand,self.market)
        await newdbtool.init()
        await newdbtool.add_sp_adGroup_negativeKeyword(self.market, None, adGroupId, campaignId, None, matchType, state,keywordText, status, datetime.now(),negativeKeywordId,keywordText,user)
        return negativeKeywordId,error_message

    async def add_adGroup_negative_keyword_batch(self,info, user = 'test'):

        adGroup_negative_keyword_info = {
          "negativeKeywords": []
        }
        for item in info:
            adGroup_negative_keyword_info["negativeKeywords"].append(
                {
                    "campaignId": str(item['campaignId']),
                    "matchType": item['matchType'],
                    "state": "ENABLED",
                    "adGroupId": str(item['adGroupId']),
                    "keywordText": item['keywordText']
                }
            )
        # api更新
        res = await self.add_adGroup_negativekw(adGroup_negative_keyword_info)
        # 存储更新记录到数据库
        dbNewTools = DbNewSpTools(self.db, self.brand, self.market)
        await dbNewTools.init()
        # 获取成功的 index
        success_indices = {item['index']: item['negativeKeywordId'] for item in res['negativeKeywords']['success']}

        updates = []
        res = []
        for idx, item in enumerate(info):
            # 检查当前的索引是否在成功的索引中
            if idx in success_indices:
                targeting_state = "success"
                target_id = success_indices[idx]
            else:
                targeting_state = "failed"
                target_id = None  # 或者设置为其他默认值

            updates.append({
                'market': self.market,
                'adGroupName': None,
                'adGroupId': item['adGroupId'],
                'campaignId': item['campaignId'],
                'campaignName': item['campaignName'],
                'matchType': item['matchType'],
                'keyword_state': "ENABLED",
                'keywordText': item['keywordText'],
                'operation_state': targeting_state,  # Assuming you have this value in `info`
                'update_time': datetime.now(),
                'campaignNegativeKeywordId': target_id,
                'keywordText_new': item['keywordText'],
                'user': user,
                'click': item['click'],
                'cpc': item['cpc'],
                'acos': item['acos']
            })
            res.append({
                'campaignId': item['campaignId'],
                'keywordText': item['keywordText'],
                'matchType': item['matchType'],
                'state': targeting_state
            })
        # 批量插入到数据库
        await dbNewTools.batch_add_sp_adGroup_negativeKeyword(updates)
        return res

    async def delete_adGroup_negative_keyword(self, adGroupNegativeKeywordId, user='test'):
        info = self.to_iterable(adGroupNegativeKeywordId)
        adGroup_info = {
            "negativeKeywordIdFilter": {
                "include": []
            }
        }
        for item in info:
            adGroup_info["negativeKeywordIdFilter"]["include"].append(str(item))
        # api更新
        res = await self.delete_adGroup_negativekw(adGroup_info)
        # 存储更新记录到数据库
        dbNewTools = DbNewSpTools(self.db, self.brand, self.market)
        await dbNewTools.init()
        # 获取成功的 index
        success_indices = {item['index']: item['negativeKeywordId'] for item in res['negativeKeywords']['success']}
        print(success_indices)
        updates = []
        for idx, item in enumerate(info):
            # 检查当前的索引是否在成功的索引中
            if idx in success_indices:
                targeting_state = "success"
                target_id = success_indices[idx]
            else:
                targeting_state = "failed"
                target_id = None  # 或者设置为其他默认值

            updates.append({
                'market': self.market,
                'keyword_state': "ARCHIVED",
                'keywordText': "Negative",
                'campaignNegativeKeywordId': item,
                'operation': "DELETE",
                'operation_state': targeting_state,
                'update_time': datetime.now(),
                'user': user
            })
            # 批量插入到数据库
        await dbNewTools.batch_update_sp_adGroup_negativeKeyword(updates)

    async def delete_keyword_toadGroup_batch(self,keywordId, user='test'):
        info = self.to_iterable(keywordId)
        # 修改广告组关键词信息
        keyword_info = {
          "keywordIdFilter": {
            "include": []
          }
        }
        for item in info:
            keyword_info["keywordIdFilter"]["include"].append(str(item))
        # 修改关键词操作
        res = await self.delete_spkeyword_api(keyword_info)

        dbNewTools = DbNewSpTools(self.db, self.brand,self.market)
        await dbNewTools.init()
        # 获取成功的 index
        success_indices = {item['index']: item['keywordId'] for item in res['keywords']['success']}
        print(success_indices)
        updates = []
        for idx, item in enumerate(info):
            # 检查当前的索引是否在成功的索引中
            if idx in success_indices:
                targeting_state = "success"
                target_id = success_indices[idx]
            else:
                targeting_state = "failed"
                target_id = None  # 或者设置为其他默认值

            updates.append({
                'market': self.market,
                'keywordId': item,
                'state': 'ARCHIVED',
                'bid_old': None,  # Assuming you have this value in `info`
                'bid_new': None,
                'operation_state': targeting_state,
                'create_time': datetime.now(),
                'user': user
            })
        # 批量插入到数据库
        await dbNewTools.batch_update_sp_keywords(updates)

    async def delete_adGroup_Targeting(self,targetId,user='test'):
        info = self.to_iterable(targetId)
        adGroup_info = {
          "targetIdFilter": {
            "include": []
          }
        }
        for item in info:
            adGroup_info["targetIdFilter"]["include"].append(str(item))
        # api更新
        res = await self.delete_targeting_api(adGroup_info)
        # 存储更新记录到数据库
        dbNewTools = DbNewSpTools(self.db, self.brand, self.market)
        await dbNewTools.init()
        # 获取成功的 index
        success_indices = {item['index']: item['targetId'] for item in res['targetingClauses']['success']}
        print(success_indices)
        updates = []
        for idx, item in enumerate(info):
            # 检查当前的索引是否在成功的索引中
            if idx in success_indices:
                targeting_state = "success"
                target_id = success_indices[idx]
            else:
                targeting_state = "failed"
                target_id = None  # 或者设置为其他默认值

            updates.append({
                'market': self.market,
                'adGroupId': None,
                'bid_old': None,
                'state': "ARCHIVED",
                'expression': item,  # Assuming you have this value in `info`
                'targetingType': 'SP',
                'targetingState': targeting_state,
                'update_time': datetime.now(),
                'user': user,
                'bid_new': None
            })
        # 批量插入到数据库
        await dbNewTools.batch_update_adGroup_Targeting(updates)

    async def delete_sku_batch(self,adId,user='test'):
        info = self.to_iterable(adId)
        adGroup_info = {
          "adIdFilter": {
            "include": []
          }
        }
        for item in info:
            adGroup_info["adIdFilter"]["include"].append(str(item))
        # api更新
        res = await self.delete_sku_api(adGroup_info)
        # 存储更新记录到数据库
        dbNewTools = DbNewSpTools(self.db, self.brand, self.market)
        await dbNewTools.init()
        # 获取成功的 index
        success_indices = {item['index']: item['adId'] for item in res['productAds']['success']}
        print(success_indices)
        updates = []
        for idx, item in enumerate(info):
            # 检查当前的索引是否在成功的索引中
            if idx in success_indices:
                targeting_state = "success"
                target_id = success_indices[idx]
            else:
                targeting_state = "failed"
                target_id = None  # 或者设置为其他默认值

            updates.append({
                'market': self.market,
                'adId': item,
                'state_new': "ARCHIVED",
                'status': targeting_state,
                'update_time': datetime.now(),  # Assuming you have this value in `info`
                'user': user,
                'campaignId': None,
                'campaignName': None,
                'click': None,
                'cpc': None,
                'acos': None
            })
        # 批量插入到数据库
        await dbNewTools.batch_update_sp_product(updates)

    async def update_adGroup_TargetingClause(self,target_id,bid,state, user='test'):
        adGroup_info = {
          "targetingClauses": [
            {
              "targetId": target_id,
              "state": state,
              "bid": bid
            }
          ]
        }
        # api更新
        res = await self.update_adGroup_TargetingC(adGroup_info)

        if isinstance(res, dict) and res['targetingClauses']['success']:
            status = "success"
            targetId = res['targetingClauses']['success'][0]['targetId']
            error_message = None
        else:
            status = "failed"
            targetId = None
            error_message = res['targetingClauses']['error'][0]['errors'][0]['errorType'] if isinstance(res, dict) else res
        # 结果写入日志
        newdbtool = DbNewSpTools(self.db, self.brand,self.market)
        await newdbtool.init()
        await newdbtool.update_sd_adGroup_Targeting(self.market, None,None, bid, state, target_id, "SP",status, datetime.now(), user)
        return error_message

    async def update_adGroup_TargetingClause_batch(self,info, user='test'):

        adGroup_info = {
            "targetingClauses": []
        }

        for item in info:
            adGroup_info["targetingClauses"].append({
                "targetId": str(item['keywordId']),
                "state": item['state'],
                "bid": item['bid_new']
            })
        print(adGroup_info)
        # 修改关键词操作
        res = await self.update_adGroup_TargetingC(adGroup_info)
        print(res)
        # 存储更新记录到数据库
        dbNewTools = DbNewSpTools(self.db, self.brand, self.market)
        await dbNewTools.init()
        # 获取成功的 index
        success_indices = {item['index']: item['targetId'] for item in res['targetingClauses']['success']}
        print(success_indices)
        updates = []
        for idx, item in enumerate(info):
            # 检查当前的索引是否在成功的索引中
            if idx in success_indices:
                targeting_state = "success"
                target_id = success_indices[idx]
            else:
                targeting_state = "failed"
                target_id = None  # 或者设置为其他默认值

            updates.append({
                'market': self.market,
                'adGroupId': None,
                'bid_old': item['bid'],
                'state': item['state'],
                'expression': item['keywordId'],  # Assuming you have this value in `info`
                'targetingType': 'SP',
                'targetingState': targeting_state,
                'update_time': datetime.now(),
                'user': user,
                'bid_new': item['bid_new']
            })
        # 批量插入到数据库
        await dbNewTools.batch_update_adGroup_Targeting(updates)

    async def create_adGroup_Targeting1(self,new_campaign_id,new_adgroup_id,asin,bid,state,type, user='test'):
        adGroup_info = {
          "targetingClauses": [
            {
              "expression": [
                {
                  "type": type,
                  "value": asin
                }
              ],
              "campaignId": new_campaign_id,
              "expressionType": "MANUAL",
              "state": state,
              "bid": bid,
              "adGroupId": new_adgroup_id
            }
          ]
        }
        # api更新
        res = await self.create_adGroup_TargetingC(adGroup_info)

        if isinstance(res, dict) and res['targetingClauses']['success']:
            status = "success"
            targetId = res['targetingClauses']['success'][0]['targetId']
            error_message = None
        else:
            status = "failed"
            targetId = None
            error_message = res['targetingClauses']['error'][0]['errors'][0]['errorType'] if isinstance(res, dict) else res
        #结果写入日志
        newdbtool = DbNewSpTools(self.db, self.brand,self.market)
        await newdbtool.init()
        await newdbtool.add_sd_adGroup_Targeting(self.market, new_adgroup_id, bid, type, state, asin, "SP",
                                               status, datetime.now(),targetId, user)
        return targetId, error_message

    async def create_adGroup_Targeting2(self,new_campaign_id,new_adgroup_id,bid,categories_id,brand_id, user='test'):
        adGroup_info = {
          "targetingClauses": [
            {
              "expression": [
                  {
                      "type": "ASIN_CATEGORY_SAME_AS",
                      "value": categories_id
                  },
                  {
                      "type": "ASIN_BRAND_SAME_AS",
                      "value": brand_id
                  }
              ],
              "campaignId": new_campaign_id,
              "expressionType": "MANUAL",
              "state": "ENABLED",
              "bid": bid,
              "adGroupId": new_adgroup_id
            }
          ]
        }
        # api更新
        res = await self.create_adGroup_TargetingC(adGroup_info)

        if isinstance(res, dict) and res['targetingClauses']['success']:
            status = "success"
            targetId = res['targetingClauses']['success'][0]['targetId']
            error_message = None
        else:
            status = "failed"
            targetId = None
            error_message = res['targetingClauses']['error'][0]['errors'][0]['errorType'] if isinstance(res, dict) else res
        #结果写入日志
        newdbtool = DbNewSpTools(self.db, self.brand,self.market)
        await newdbtool.init()
        expression = f"Category={categories_id},brand={brand_id}"
        await newdbtool.add_sd_adGroup_Targeting(self.market, new_adgroup_id, bid, "MANUAL", "ENABLED", expression, "SP",
                                           status, datetime.now(),targetId, user)
        return targetId, error_message

    async def create_adGroup_Targeting3(self,new_campaign_id,new_adgroup_id,bid,categories_id, user='test'):
        adGroup_info = {
          "targetingClauses": [
            {
              "expression": [
                  {
                      "type": "ASIN_CATEGORY_SAME_AS",
                      "value": categories_id
                  }
              ],
              "campaignId": new_campaign_id,
              "expressionType": "MANUAL",
              "state": "ENABLED",
              "bid": bid,
              "adGroupId": new_adgroup_id
            }
          ]
        }
        # api更新
        res = await self.create_adGroup_TargetingC(adGroup_info)

        if isinstance(res, dict) and res['targetingClauses']['success']:
            status = "success"
            targetId = res['targetingClauses']['success'][0]['targetId']
            error_message = None
        else:
            status = "failed"
            targetId = None
            error_message = res['targetingClauses']['error'][0]['errors'][0]['errorType'] if isinstance(res, dict) else res
        #结果写入日志
        newdbtool = DbNewSpTools(self.db, self.brand,self.market)
        await newdbtool.init()
        expression = f"Category={categories_id}"
        await newdbtool.add_sd_adGroup_Targeting(self.market, new_adgroup_id, bid, "MANUAL", "ENABLED", expression, "SP",
                                           status, datetime.now(),targetId, user,new_campaign_id)
        return targetId, error_message

    async def create_adGroup_Negative_Targeting_by_asin(self,new_campaign_id,new_adgroup_id,asin,user='test'):
        adGroup_info = {
          "negativeTargetingClauses": [
            {
              "expression": [
                {
                  "type": "ASIN_SAME_AS",
                  "value": asin
                }
              ],
              "campaignId": str(new_campaign_id),
              "state": "ENABLED",
              "adGroupId": str(new_adgroup_id)
            }
          ]
        }
        # api更新
        res = await self.create_adGroup_Negative_TargetingClauses(adGroup_info)

        if isinstance(res, dict) and res['negativeTargetingClauses']['success']:
            status = "success"
            targetId = res['negativeTargetingClauses']['success'][0]['targetId']
            error_message = None
        else:
            status = "failed"
            targetId = None
            error_message = res['negativeTargetingClauses']['error'][0]['errors'][0]['errorType'] if isinstance(res, dict) else res
        #结果写入日志
        newdbtool = DbNewSpTools(self.db, self.brand,self.market)
        await newdbtool.init()
        expression = f"asin={asin}"
        await newdbtool.add_sd_adGroup_Targeting(self.market, new_adgroup_id, None, "Negative", "ENABLED", expression, "SP",
                                               status, datetime.now(),targetId,user)
        return targetId,error_message

    async def create_adGroup_Negative_Targeting_by_asin_batch(self,info,user='test'):
        adGroup_info = {
          "negativeTargetingClauses": []
        }
        for item in info:
            adGroup_info["negativeTargetingClauses"].append({
                    "expression": [
                        {
                            "type": "ASIN_SAME_AS",
                            "value": str(item['asin'])
                        }
                    ],
                    "campaignId": str(item['campaignId']),
                    "state": "ENABLED",
                    "adGroupId": str(item['adGroupId'])
            })

        # api更新
        res = await self.create_adGroup_Negative_TargetingClauses(adGroup_info)
        #结果写入日志
        print(res)
        # 存储更新记录到数据库
        dbNewTools = DbNewSpTools(self.db, self.brand, self.market)
        await dbNewTools.init()
        # 获取成功的 index
        success_indices = {item['index']: item['targetId'] for item in res['negativeTargetingClauses']['success']}
        print(success_indices)
        updates = []
        res = []
        for idx, item in enumerate(info):
            # 检查当前的索引是否在成功的索引中
            if idx in success_indices:
                targeting_state = "success"
                target_id = success_indices[idx]
            else:
                targeting_state = "failed"
                target_id = None  # 或者设置为其他默认值

            updates.append({
                'market': self.market,
                'adGroupId': item['adGroupId'],
                'bid': None,
                'expressionType': "Negative",
                'state': "ENABLED",
                'expression': f"asin={item['asin']}",  # Assuming you have this value in `info`
                'targetingType': "SP",
                'targetingState': targeting_state,
                'update_time': datetime.now(),
                'user': user,
                'targetId': target_id,
                'campaignId': item['campaignId'],
                'campaignName': item['campaignName'],
                'click': item['click'],
                'cpc': item['cpc'],
                'acos': item['acos']
            })
            res.append({
                'campaignId': item['campaignId'],
                'keywordText': item['asin'],
                'matchType': "ASIN_SAME_AS",
                'state': targeting_state
            })

        # 批量插入到数据库
        await dbNewTools.batch_add_sd_adGroup_Targeting(updates)
        return res

    async def delete_adGroup_Negative_Targeting(self,targetId,user='test'):
        info = self.to_iterable(targetId)
        adGroup_info = {
          "negativeTargetIdFilter": {
            "include": []
          }
        }
        for item in info:
            adGroup_info["negativeTargetIdFilter"]["include"].append(str(item))
        # api更新
        res = await self.delete_adGroup_Negative_TargetingClauses(adGroup_info)
        # 存储更新记录到数据库
        dbNewTools = DbNewSpTools(self.db, self.brand, self.market)
        await dbNewTools.init()
        # 获取成功的 index
        success_indices = {item['index']: item['targetId'] for item in res['negativeTargetingClauses']['success']}
        print(success_indices)
        updates = []
        for idx, item in enumerate(info):
            # 检查当前的索引是否在成功的索引中
            if idx in success_indices:
                targeting_state = "success"
                target_id = success_indices[idx]
            else:
                targeting_state = "failed"
                target_id = None  # 或者设置为其他默认值

            updates.append({
                'market': self.market,
                'adGroupId': "Negative",
                'bid_old': None,
                'state': "ARCHIVED",
                'expression': item,  # Assuming you have this value in `info`
                'targetingType': 'SP',
                'targetingState': targeting_state,
                'update_time': datetime.now(),
                'user': user,
                'bid_new': None
            })
        # 批量插入到数据库
        await dbNewTools.batch_update_adGroup_Targeting(updates)

    async def create_productsku(self,campaignId,adGroupId,sku,asin,state,user='test'):
        product_info = {
          "productAds": [
            {
              "campaignId": str(campaignId),
              "state": state,
              "sku": sku,
              "asin": asin,
              "adGroupId": str(adGroupId)
            }
          ]
        }
        # 执行新增品 返回adId
        res = await self.create_product_api(product_info)

        if isinstance(res, dict) and res['productAds']['success']:
            status = "success"
            adId = res['productAds']['success'][0]['adId']
            error_message = None
        else:
            status = "failed"
            adId = None
            error_message = res['productAds']['error'][0]['errors'][0]['errorType'] if isinstance(res, dict) else res
        # 如果执行成功或者失败 记录到log表记录
        dbNewTools = DbNewSpTools(self.db, self.brand,self.market)
        await dbNewTools.init()
        await dbNewTools.create_sp_product(self.market,campaignId,asin,sku,adGroupId,adId,status,datetime.now(),"SP",user)
        return adId, error_message

    async def create_productsku_batch(self,info,user='test'):
        product_info = {
          "productAds": []
        }
        for item in info:
            product_info["productAds"].append({
              "campaignId": str(item['campaignId']),
              "state": "ENABLED",
              "adGroupId": str(item['adGroupId']),
              "sku": item['sku']
            })
        # 执行新增品 返回adId
        res = await self.create_product_api(product_info)
        success_indices = {item['index']: item['adId'] for item in res['productAds']['success']}
        updates = []
        res = []
        # 如果执行成功或者失败 记录到log表记录
        dbNewTools = DbNewSpTools(self.db, self.brand,self.market)
        await dbNewTools.init()
        for idx, item in enumerate(info):
            # 检查当前的索引是否在成功的索引中
            if idx in success_indices:
                targeting_state = "success"
                adId = success_indices[idx]
            else:
                targeting_state = "failed"
                adId = None  # 或者设置为其他默认值
            updates.append({
                'market': self.market,
                'campaignId': item['campaignId'],
                'asin': None,
                'sku': item['sku'],
                'adGroupId': item['adGroupId'],
                'adId': adId,
                'status': targeting_state,
                'update_time': datetime.now(),
                'productType': "SP",
                'user': user
            })
            res.append({
                'sku': item['sku'],
                'adId': adId,
                'state': targeting_state,
            })
        # 批量插入到数据库
        await dbNewTools.batch_create_sp_product(updates)
        return res

    async def update_product(self,adId,state, user='test',campaignId=None,campaignName=None,click=None,cpc=None,acos=None):
        product_info = {
            "productAds": [
                {
                    "adId": adId,
                    "state": state
                }
            ]
        }
        # 执行修改品
        res = await self.update_product_api(product_info)
        if isinstance(res, dict) and res['productAds']['success']:
            status = "success"
            adId = res['productAds']['success'][0]['adId']
            error_message = None
        else:
            status = "failed"
            adId = None
            error_message = res['productAds']['error'][0]['errors'][0]['errorType'] if isinstance(res, dict) else res
        # 如果执行成功或者失败 记录到log表记录
        dbNewTools = DbNewSpTools(self.db, self.brand,self.market)
        await dbNewTools.init()
        await dbNewTools.update_sp_product(self.market, adId, state, status, datetime.now(), user,campaignId,campaignName,click,cpc,acos)
        return error_message


    async def update_product_batch(self,info, user='test'):
        product_info = {
            "productAds": []
        }
        for item in info:
            product_info["productAds"].append({
                    "adId": str(item['adId']),
                    "state": str(item['statu'])
            })
        # 执行新增品 返回adId
        res = await self.update_product_api(product_info)
        success_indices = {item['index']: item['adId'] for item in res['productAds']['success']}
        updates = []
        res = []
        # 如果执行成功或者失败 记录到log表记录
        dbNewTools = DbNewSpTools(self.db, self.brand, self.market)
        await dbNewTools.init()
        for idx, item in enumerate(info):
            # 检查当前的索引是否在成功的索引中
            if idx in success_indices:
                targeting_state = "success"
                adId = success_indices[idx]
            else:
                targeting_state = "failed"
                adId = None  # 或者设置为其他默认值
            updates.append({
                'market': self.market,
                'adId': str(item['adId']),
                'state_new': str(item['statu']),
                'status': targeting_state,
                'update_time': datetime.now(),  # Assuming you have this value in `info`
                'user': user,
                'campaignId': item['campaignId'],
                'campaignName': item['campaignName'],
                'click': item['click'],
                'cpc': item['cpc'],
                'acos': item['acos']
            })
            # 批量插入到数据库
            res.append({
                'sku': item['sku'],
                'adId': adId,
                'state':  str(item['statu']),
                'status': targeting_state,
            })
        await dbNewTools.batch_update_sp_product(updates)
        return res

    async def add_keyword_toadGroup_v0(self,campaignId,adGroupId,keywordText,matchType,state,bid, user='test'):
        # 翻译完成进行添加
        keyword_info={
          "keywords": [
            {
              "campaignId": str(campaignId),
              "matchType": matchType,
              "state": state,
              "bid": bid,
              "adGroupId": str(adGroupId),
              "keywordText": keywordText
            }
          ]
        }
        # 新增关键词操作
        res = await self.create_spkeyword_api(keyword_info)
        if isinstance(res, dict) and res['keywords']['success']:
            status = "success"
            keywordId = res['keywords']['success'][0]['keywordId']
            error_message = None
        else:
            status = "failed"
            keywordId = None
            error_message = res['keywords']['error'][0]['errors'][0]['errorType'] if isinstance(res, dict) else res
        # 根据结果更新log
        dbNewTools = DbNewSpTools(self.db, self.brand,self.market)
        await dbNewTools.init()
        await dbNewTools.add_sp_keyword_toadGroup(self.market,keywordId,campaignId,matchType,state,bid,adGroupId,None,keywordText,status,datetime.now(), user)
        return keywordId, error_message

    async def update_keyword_toadGroup(self,keywordId,bid_old,bid_new,state, user='test'):
        # 修改广告组关键词信息
        keyword_info = {
          "keywords": [
            {
              "keywordId": str(keywordId),
              "state": state,
              "bid": bid_new
            }
          ]
        }
        # 修改关键词操作
        res = await self.update_spkeyword_api(keyword_info)
        if isinstance(res, dict) and res['keywords']['success']:
            status = "success"
            keywordId = res['keywords']['success'][0]['keywordId']
            error_message = None
        else:
            status = "failed"
            keywordId = None
            error_message = res['keywords']['error'][0]['errors'][0]['errorType'] if isinstance(res, dict) else res
        # 根据结果更新log
        # def update_sp_keyword_toadGroup(self,market,keywordId,state,bid,operation_state,create_time):
        dbNewTools = DbNewSpTools(self.db, self.brand,self.market)
        await dbNewTools.init()
        await dbNewTools.update_sp_keyword_toadGroup(self.market,keywordId,state,bid_old,bid_new,status,datetime.now(), user)
        return error_message

    async def update_keyword_toadGroup_batch(self,info, user='test'):
        keyword_info = {
            "keywords": []
        }

        for item in info:
            keyword_info["keywords"].append({
                "keywordId": str(item['keywordId']),
                "state": item['state'],
                "bid": item['bid_new']
            })
        print(keyword_info)
        # 修改关键词操作
        res = await self.update_spkeyword_api(keyword_info)
        print(res)
        # 存储更新记录到数据库
        dbNewTools = DbNewSpTools(self.db, self.brand, self.market)
        await dbNewTools.init()
        # 获取成功的 index
        success_indices = {item['index']: item['keywordId'] for item in res['keywords']['success']}
        print(success_indices)
        updates = []
        for idx, item in enumerate(info):
            # 检查当前的索引是否在成功的索引中
            if idx in success_indices:
                targeting_state = "success"
                target_id = success_indices[idx]
            else:
                targeting_state = "failed"
                target_id = None  # 或者设置为其他默认值

            updates.append({
                'market': self.market,
                'keywordId': item['keywordId'],
                'state': item['state'],
                'bid_old': item['bid'],  # Assuming you have this value in `info`
                'bid_new': item['bid_new'],
                'operation_state': targeting_state,
                'create_time': datetime.now(),
                'user': user
            })
        # 批量插入到数据库
        await dbNewTools.batch_update_sp_keywords(updates)

    async def add_keyword_toadGroup_batch(self,info, user='test'):
        # 翻译完成进行添加
        keyword_info = {
          "keywords": []
        }
        for item in info:
            keyword_info["keywords"].append({
              "campaignId": str(item['campaignId']),
              "matchType": item['matchType'],
              "state": "ENABLED",
              "bid": float(item['bid']),
              "adGroupId": str(item['adGroupId']),
              "keywordText": item['keywordText']
            })
        # 新增关键词操作
        res = await self.create_spkeyword_api(keyword_info)
        print(res)
        # 存储更新记录到数据库
        dbNewTools = DbNewSpTools(self.db, self.brand, self.market)
        await dbNewTools.init()
        # 获取成功的 index
        success_indices = {item['index']: item['keywordId'] for item in res['keywords']['success']}
        print(success_indices)
        updates = []
        res = []
        for idx, item in enumerate(info):
            # 检查当前的索引是否在成功的索引中
            if idx in success_indices:
                targeting_state = "success"
                keywordId = success_indices[idx]
            else:
                targeting_state = "failed"
                keywordId = None  # 或者设置为其他默认值
            print(targeting_state,keywordId)
            updates.append({
                'market': self.market,
                'keywordId': keywordId,
                'campaignId': item['campaignId'],
                'matchType': item['matchType'],
                'state': "ENABLED",
                'bid': item['bid'],  # Assuming you have this value in `info`
                'adGroupId': item['adGroupId'],
                'keywordText': None,
                'keywordText_new': item['keywordText'],
                'operation_state': targeting_state,
                'create_time': datetime.now(),
                'user': user
            })
            res.append({
                'keywordText': item['keywordText'],
                'matchType': item['matchType'],
                'bid': item['bid'],
                'state': targeting_state,
            })
        # 批量插入到数据库
        await dbNewTools.batch_add_sp_keyword_toadGroup(updates)
        return res

    async def create_adGroup_Targeting_by_asin_batch(self,info,user='test'):
        adGroup_info = {
          "targetingClauses": []
        }
        for item in info:
            adGroup_info["targetingClauses"].append({
                    "expression": [
                        {
                            "type": str(item['type']),
                            "value": str(item['asin'])
                        }
                    ],
                    "campaignId": str(item['campaignId']),
                    "expressionType": "MANUAL",
                    "state": "ENABLED",
                    "bid": float(item['bid']),
                    "adGroupId": str(item['adGroupId'])
            })

        # api更新
        res = await self.create_adGroup_TargetingC(adGroup_info)
        #结果写入日志
        print(res)
        # 存储更新记录到数据库
        dbNewTools = DbNewSpTools(self.db, self.brand, self.market)
        await dbNewTools.init()
        # 获取成功的 index
        success_indices = {item['index']: item['targetId'] for item in res['targetingClauses']['success']}
        print(success_indices)
        updates = []
        res = []
        for idx, item in enumerate(info):
            # 检查当前的索引是否在成功的索引中
            if idx in success_indices:
                targeting_state = "success"
                target_id = success_indices[idx]
            else:
                targeting_state = "failed"
                target_id = None  # 或者设置为其他默认值

            updates.append({
                'market': self.market,
                'adGroupId': item['adGroupId'],
                'bid': item['bid'],
                'expressionType': "MANUAL",
                'state': "ENABLED",
                'expression': f"{item['type']}={item['asin']}",  # Assuming you have this value in `info`
                'targetingType': "SP",
                'targetingState': targeting_state,
                'update_time': datetime.now(),
                'user': user,
                'targetId': target_id,
                'campaignId': item['campaignId'],
                'campaignName': None,
                'click': None,
                'cpc': None,
                'acos': None
            })
            res.append({
                'keywordText': item['asin'],
                'matchType': item['type'],
                'bid': item['bid'],
                'state': targeting_state,
            })
        # 批量插入到数据库
        await dbNewTools.batch_add_sd_adGroup_Targeting(updates)
        return res

if __name__ == "__main__":
    #GenCampaign('amazon_ads','LAPASA','US').create_camapign('DeepBI_AUTO_test','2024-10-14',None,None,None,'AUTO','PAUSED','DAILY',10)
    async def main():
        res = await GenCampaign('amazon_ads', 'LAPASA', 'US').create_camapign('DeepBI_AUTO_test', '2024-10-14', None, None,
                                                                        None, 'AUTO', 'PAUSED', 'DAILY', 10)
        print(res)


    # 在主函数中运行异步任务
    asyncio.run(main())