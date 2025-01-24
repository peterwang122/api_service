import asyncio
import multiprocessing
import threading
import traceback
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import os
import pandas as pd
import json
import yaml
from api.ad_api.sp.gen_sp import GenSP
from api.ad_api.sp.tools_sp import ToolsSP
from logs.logger import logger
from util.expanded_asin import expanded_asin
from util.searchterm_asin2 import searchterm_asin


class auto_api_sp:
    def __init__(self, brand, market, db, user):
        self.brand = brand
        self.market = market
        self.db = db
        self.user = user

    async def update_sp_ad_budget(self, campaignId, bid):
        try:
            api1 = GenSP(self.db, self.brand, self.market)
            campaign_info = await api1.list_campaigns_api(campaignId)
            if campaign_info["campaigns"] is not None:
                for item in campaign_info["campaigns"]:
                    campaignId = item['campaignId']
                    name = item['name']
                    state = item['state']
                    bid1 = item['budget']['budget']
                    e = await api1.update_camapign_v0(str(campaignId), name, float(bid1), float(bid), state, self.user)
                    if e:
                        return 400,e
                    else:
                        return 200,e
            else:
                return 404, "Campaign not found"  # Campaign not found
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500,e  # Internal Server Error

    async def update_sp_ad_budget_batch(self, campaignId, bid):
        try:
            api = GenSP(self.db, self.brand, self.market)
            campaign_info = await api.list_campaigns_api_batch(campaignId)
            campaign_bid_mapping = {k: v for k, v in zip(campaignId, bid)}
            if campaign_info["campaigns"] is not None:
                merged_info = []
                for info in campaign_info["campaigns"]:
                    campaign_Id = info['campaignId']
                    if campaign_Id in campaign_bid_mapping:
                        merged_info.append({
                            "campaignId": campaign_Id,
                            "campaign_name": info['name'],
                            "state": info["state"],
                            "bid": info['budget']['budget'],
                            "bid_new": float(campaign_bid_mapping[campaign_Id])  # 从 mapping 中获取 bid_old
                        })
                await api.update_camapign_batch(merged_info, self.user)
                return 200,None
            else:
                return 404,"Campaign not found"  # Keyword not found
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500,e  # Internal Server Error

    async def update_sp_ad_placement(self, campaignId, bid, placementClassification):
        try:
            api1 = GenSP(self.db, self.brand, self.market)
            campaign_info = await api1.list_campaigns_api(campaignId)
            if campaign_info["campaigns"] is not None:
                for item in campaign_info["campaigns"]:
                    placement_bidding = item['dynamicBidding']['placementBidding']
                    possible_placements = ['PLACEMENT_REST_OF_SEARCH', 'PLACEMENT_PRODUCT_PAGE', 'PLACEMENT_TOP']
                    placement_percentages = {placement: 0 for placement in possible_placements}
                    for item1 in placement_bidding:
                        placement = item1['placement']
                        percentage = item1['percentage']
                        if placement in possible_placements:
                            placement_percentages[placement] = percentage
                    campaignId = item['campaignId']
                    for placement, percentage in placement_percentages.items():
                        if placement == placementClassification:
                            print(f'Placement: {placement}, Percentage: {percentage}')
                            bid1 = percentage
                            if bid1 is not None:
                                e = await api1.update_campaign_placement(str(campaignId), bid1, float(bid), placement, self.user)
                                if e:
                                    return 400, e
                                else:
                                    return 200, e
            else:
                return 404,"Campaign not found"  # Campaign not found
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500,e  # Internal Server Error

    async def update_sp_ad_keyword(self, keywordId, bid):
        try:
            api = GenSP(self.db, self.brand, self.market)
            spkeyword_info = await api.get_spkeyword_api_by_keywordId(keywordId)
            if spkeyword_info["keywords"] is not None:
                for spkeyword in spkeyword_info["keywords"]:
                    bid1 = spkeyword.get('bid')
                    state = spkeyword['state']
                    e = await api.update_keyword_toadGroup(str(keywordId), bid1, float(bid), state, self.user)
                    if e:
                        return 400, e
                    else:
                        return 200, e
            else:
                return 404,"Keyword not found"  # Keyword not found
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500,e  # Internal Server Error

    async def update_sp_ad_keyword_batch(self, keywordId, bid):
        try:
            api = GenSP(self.db, self.brand, self.market)
            spkeyword_info = await api.get_spkeyword_api_by_keywordId_batch(keywordId)
            keyword_bid_mapping = {k: v for k, v in zip(keywordId, bid)}
            if spkeyword_info["keywords"] is not None:
                merged_info = []
                for info in spkeyword_info["keywords"]:
                    keyword_id = info['keywordId']
                    if keyword_id in keyword_bid_mapping:
                        merged_info.append({
                            "keywordId": keyword_id,
                            "state": info["state"],
                            "bid": info.get('bid', None),
                            "bid_new": float(keyword_bid_mapping[keyword_id])  # 从 mapping 中获取 bid_old
                        })
                await api.update_keyword_toadGroup_batch(merged_info, self.user)
                return 200,None
            else:
                return 404,"Keyword not found"  # Keyword not found
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500,e  # Internal Server Error

    async def update_sp_ad_automatic_targeting(self, keywordId, bid):
        try:
            api1 = GenSP(self.db, self.brand, self.market)
            automatic_targeting_info = await api1.list_adGroup_TargetingClause_by_targetId(keywordId)
            if automatic_targeting_info["targetingClauses"] is not None:
                for item in automatic_targeting_info["targetingClauses"]:
                    targetId = item['targetId']
                    state = item['state']
                    bid1 = item.get('bid')
                    e = await api1.update_adGroup_TargetingClause(str(targetId), float(bid), state, self.user)
                    if e:
                        return 400, e
                    else:
                        return 200, e
            else:
                return 404,"Targeting not found"  # Targeting not found
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500,e  # Internal Server Error

    async def update_sp_ad_automatic_targeting_batch(self, keywordId, bid):
        try:
            api1 = GenSP(self.db, self.brand, self.market)
            automatic_targeting_info = await api1.list_adGroup_TargetingClause_by_targetId_batch(keywordId)
            keyword_bid_mapping = {k: v for k, v in zip(keywordId, bid)}
            if automatic_targeting_info["targetingClauses"] is not None:
                merged_info = []
                for info in automatic_targeting_info["targetingClauses"]:
                    keyword_id = info['targetId']
                    if keyword_id in keyword_bid_mapping:
                        merged_info.append({
                            "keywordId": keyword_id,
                            "state": info["state"],
                            "bid": info.get('bid', None),
                            "bid_new": float(keyword_bid_mapping[keyword_id]) # 从 mapping 中获取 bid_old
                        })
                await api1.update_adGroup_TargetingClause_batch(merged_info, self.user)
                return 200,None
            else:
                return 404,"Keyword not found"  # Keyword not found
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500,e  # Internal Server Error

    async def update_sp_ad_product_targets(self, keywordId, bid):
        try:
            api1 = GenSP(self.db, self.brand, self.market)
            automatic_targeting_info = await api1.list_adGroup_TargetingClause_by_targetId(keywordId)
            if automatic_targeting_info["targetingClauses"] is not None:
                for automatic_targeting in automatic_targeting_info["targetingClauses"]:
                    targetId = automatic_targeting['targetId']
                    state = automatic_targeting['state']
                    bid1 = automatic_targeting.get('bid')
                    e = await api1.update_adGroup_TargetingClause(str(targetId), float(bid), state, self.user)
                    if e:
                        return 400, e
                    else:
                        return 200, e
            else:
                return 404,"Targeting not found"  # Targeting not found
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500,e  # Internal Server Error

    async def auto_campaign_status(self, campaignId, status):
        try:
            api1 = GenSP(self.db, self.brand, self.market)
            campaign_info = await api1.list_campaigns_api(campaignId)
            if campaign_info["campaigns"] is not None:
                for item in campaign_info["campaigns"]:
                    campaignId = item['campaignId']
                    name = item['name']
                    state = item['state']
                    e = await api1.update_camapign_status(str(campaignId), name, state, status, self.user)
                    if e:
                        return 400, e
                    else:
                        return 200, e
            else:
                return 404,"Campaign not found"  # Campaign not found
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500,e  # Internal Server Error

    async def auto_adgroup_status(self, adGroupId, status):
        try:
            api1 = GenSP(self.db, self.brand, self.market)
            adGroup_info = await api1.get_adGroup_api(adGroupId)
            if adGroup_info["adGroups"] is not None:
                for item in adGroup_info["adGroups"]:
                    adGroup_Id = item['adGroupId']
                    name = item['name']
                    state = item['state']
                    e = await api1.update_adgroup(name, str(adGroup_Id), state, status, self.user)
                    if e:
                        return 400, e
                    else:
                        return 200, e
            else:
                return 404,"adGroup not found"  # Campaign not found
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500,e  # Internal Server Error

    async def auto_sku_status(self, adId, status):
        try:
            api = GenSP(self.db, self.brand, self.market)
            e = await api.update_product(str(adId), status, self.user)
            if e:
                return 400, e
            else:
                return 200, e
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500,e  # Internal Server Error

    async def auto_sku_status_task(self, adId, status,campaignId,campaignName,click,cpc,acos):
        try:
            api = GenSP(self.db, self.brand, self.market)
            e = await api.update_product(str(adId), status, self.user,campaignId,campaignName,click,cpc,acos)
            if e:
                return 400, e
            else:
                return 200, e
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500,e  # Internal Server Error

    async def auto_keyword_status(self, keywordId, status):
        try:
            api = GenSP(self.db, self.brand, self.market)
            e = await api.update_keyword_toadGroup(str(keywordId), None, bid_new=None, state=status, user=self.user)
            if e:
                return 400, e
            else:
                return 200, e
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500,e  # Internal Server Error
    async def auto_keyword_status_batch(self, keywordId, status):
        try:
            api = GenSP(self.db, self.brand, self.market)
            merged_info = []
            for keywordid, statu in zip(keywordId, status):
                merged_info.append({
                            "keywordId": keywordid,
                            "state": statu,
                            "bid": None,
                            "bid_new": None  # 从 mapping 中获取 bid_old
                        })
            await api.update_keyword_toadGroup_batch(merged_info, self.user)
            return 200,None
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500,e  # Internal Server Error

    async def auto_targeting_status_batch(self, keywordId, status):
        try:
            api = GenSP(self.db, self.brand, self.market)
            merged_info = []
            for keywordid, statu in zip(keywordId, status):
                merged_info.append({
                            "keywordId": keywordid,
                            "state": statu,
                            "bid": None,
                            "bid_new": None  # 从 mapping 中获取 bid_old
                        })
            await api.update_adGroup_TargetingClause_batch(merged_info, self.user)
            return 200,None
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500,e  # Internal Server Error

    async def auto_sku_status_task_batch(self, adIds, status, campaignIds, campaignNames, clicks, cpcs, acoss):
        try:
            api = GenSP(self.db, self.brand, self.market)
            merged_info = []
            for adId, statu, campaignId, campaignName, click, cpc, acos in zip(adIds, status, campaignIds,
                                                                               campaignNames, clicks, cpcs, acoss):
                merged_info.append({
                        "adId": adId,
                        "campaignId": campaignId,
                        "statu": statu,
                        "campaignName": campaignName,
                        "click": click,
                        "cpc": cpc,
                        "acos": acos
                    })
            res = await api.update_product_batch(merged_info, self.user)
            return 200, res
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500, e  # Internal Server Error

    # def negative_keyword_status(self, keywordId, status):
    #     try:
    #         api = GenSP(self.db, self.brand, self.market)
    #         api.update_adGroup_negative_keyword(str(keywordId), status, user=self.user)
    #         return 200
    #     except Exception as e:
    #         logger.error(f"{traceback.format_exc()}")
    #         return 500  # Internal Server Error

    async def auto_targeting_status(self, keywordId, status):
        try:
            api1 = GenSP(self.db, self.brand, self.market)
            e = await api1.update_adGroup_TargetingClause(str(keywordId), bid=None, state=status, user=self.user)
            if e:
                return 400, e
            else:
                return 200, e
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500,e  # Internal Server Error

    # def negative_target_status(self, keywordId, status):
    #     try:
    #         api1 = GenSP(self.db, self.brand, self.market)
    #         api1.update_adGroup_Negative_Targeting(str(keywordId), status, user=self.user)
    #         return 200
    #     except Exception as e:
    #         logger.error(f"{traceback.format_exc()}")
    #         return 500,e  # Internal Server Error

    async def delete_negative_target(self, keywordId):
        try:
            api1 = GenSP(self.db, self.brand, self.market)
            await api1.delete_adGroup_Negative_Targeting(keywordId, user=self.user)
            return 200,None
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500,e  # Internal Server Error

    async def delete_negative_keyword(self, keywordId):
        try:
            api1 = GenSP(self.db, self.brand, self.market)
            await api1.delete_adGroup_negative_keyword(keywordId, user=self.user)
            return 200,None
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500,e  # Internal Server Error

    async def delete_keyword(self, keywordId):
        try:
            api1 = GenSP(self.db, self.brand, self.market)
            await api1.delete_keyword_toadGroup_batch(keywordId, user=self.user)
            return 200,None
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500,e  # Internal Server Error

    async def delete_product_target(self, keywordId):
        try:
            api1 = GenSP(self.db, self.brand, self.market)
            await api1.delete_adGroup_Targeting(keywordId, user=self.user)
            return 200,None
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500,e  # Internal Server Error

    async def delete_sku(self, keywordId):
        try:
            api1 = GenSP(self.db, self.brand, self.market)
            await api1.delete_sku_batch(keywordId, user=self.user)
            return 200,None
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500,e  # Internal Server Error

    # async def delete_sku(self, keywordId):
    #     try:
    #         api1 = GenSP(self.db, self.brand, self.market)
    #         asyncio.run(api1.delete_sku_batch(keywordId, user=self.user))
    #         return 200,None
    #     except Exception as e:
    #         logger.error(f"{traceback.format_exc()}")
    #         return 500,e  # Internal Server Error


    async def create_product_target(self, keywordId, bid, campaignId, adGroupId):
        try:
            apitool1 = ToolsSP(self.db, self.brand, self.market)
            api2 = GenSP(self.db, self.brand, self.market)
            brand_info = await apitool1.list_category_refinements(keywordId)
            # 检查是否存在名为"LAPASA"的品牌
            target_brand_name = self.brand
            target_brand_id = None

            for brand in brand_info['brands']:
                if brand['name'] == target_brand_name:
                    target_brand_id = brand['id']
                    targetId,e = await api2.create_adGroup_Targeting2(campaignId, adGroupId,
                                                              float(bid),
                                                              keywordId, target_brand_id, self.user)
                    if e:
                        return 400, e
                    else:
                        return 200, e
            return 200,"category no brand"
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500,e  # Internal Server Error

    async def create_category(self, keywordId, bid, campaignId, adGroupId):
        try:
            api2 = GenSP(self.db, self.brand, self.market)
            targetId,e = await api2.create_adGroup_Targeting3(campaignId, adGroupId,
                                                      float(bid),
                                                      keywordId, self.user)
            if e:
                return 400, e
            else:
                return 200, e
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500,e  # Internal Server Error

    async def create_product_target_asin(self, asin, bid, campaignId, adGroupId):
        try:
            api2 = GenSP(self.db, self.brand, self.market)
            targetId,e = await api2.create_adGroup_Targeting1(campaignId, adGroupId, asin, float(bid),
                                           state='ENABLED', type='ASIN_SAME_AS', user=self.user)
            if e:
                return 400, e
            else:
                return 200, e
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500,e  # Internal Server Error

    async def create_product_target_asin_expended(self, asin, bid, campaignId, adGroupId):
        try:
            api2 = GenSP(self.db, self.brand, self.market)
            targetId,e = await api2.create_adGroup_Targeting1(campaignId, adGroupId, asin, float(bid),
                                           state='ENABLED', type='ASIN_EXPANDED_FROM', user=self.user)
            if e:
                return 400, e
            else:
                return 200, e
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500,e  # Internal Server Error

    async def create_keyword(self, keywordtext, bid, campaignId, adGroupId,matchType):
        try:
            api2 = GenSP(self.db, self.brand, self.market)
            targetId,e = await api2.add_keyword_toadGroup_v0(campaignId, adGroupId, keywordtext, matchType,
                                           'ENABLED', float(bid), self.user)
            if e:
                return 400, e
            else:
                return 200, e
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500,e  # Internal Server Error

    async def create_negative_target(self, searchTerm, campaignId, adGroupId,matchType):
        try:
            api1 = GenSP(self.db, self.brand, self.market)
            if len(searchTerm) == 10 and searchTerm.startswith('B0'):
                targetId,e = await api1.create_adGroup_Negative_Targeting_by_asin(str(campaignId), str(adGroupId), searchTerm.upper(), user=self.user)
            else:
                targetId,e = await api1.add_adGroup_negative_keyword_v0(str(campaignId), str(adGroupId), searchTerm,
                                                         matchType=matchType, state="ENABLED", user=self.user)
            if e:
                return 400, e
            else:
                return 200, e
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500,e  # Internal Server Error

    async def create_keyword_batch(self, keyWord, Bid, campaignId, adGroupId,matchType):
        try:
            api1 = GenSP(self.db, self.brand, self.market)
            merged_keyword_info = []
            for keyword, bid, campaignid, adGroupid, matchtype in zip(keyWord, Bid, campaignId,
                                                                       adGroupId, matchType):
                merged_keyword_info.append({
                    "keywordText": keyword,
                    "bid": bid,
                    "campaignId": campaignid,
                    "adGroupId": adGroupid,
                    "matchType": matchtype  # 从 mapping 中获取 bid_old
                })

            res = await api1.add_keyword_toadGroup_batch(merged_keyword_info, user=self.user)
            return 200,res
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500,e  # Internal Server Error

    async def create_product_target_batch(self, keyWord, Bid, campaignId, adGroupId,matchType):
        try:
            api1 = GenSP(self.db, self.brand, self.market)
            merged_keyword_info = []
            for keyword, bid, campaignid, adGroupid, matchtype in zip(keyWord, Bid, campaignId,
                                                                       adGroupId, matchType):
                merged_keyword_info.append({
                    "type": matchtype,
                    "asin": keyword,
                    "bid": bid,
                    "campaignId": campaignid,
                    "adGroupId": adGroupid,
                })

            res = await api1.create_adGroup_Targeting_by_asin_batch(merged_keyword_info, user=self.user)
            return 200,res
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500,e  # Internal Server Error

    async def create_negative_target_batch(self, searchTerm, campaignId, adGroupId, matchType, campaignNames, clicks, cpcs, acoss):
        try:
            api1 = GenSP(self.db, self.brand, self.market)
            merged_asin_info = []
            merged_keyword_info = []
            for searchterm, campaignid, adGroupid, matchtype, campaignName, click, cpc, acos in zip(searchTerm, campaignId,
                                                                       adGroupId, matchType,campaignNames,clicks,cpcs,acoss):
                if len(searchterm) == 10 and searchterm.startswith('B0'):
                    merged_asin_info.append({
                        "asin": searchterm,
                        "campaignId": campaignid,
                        "adGroupId": adGroupid,
                        "campaignName": campaignName,
                        "click": click,
                        "cpc": cpc,
                        "acos": acos
                    })
                else:
                    merged_keyword_info.append({
                        "keywordText": searchterm,
                        "campaignId": campaignid,
                        "adGroupId": adGroupid,
                        "matchType": matchtype,  # 从 mapping 中获取 bid_old
                        "campaignName": campaignName,
                        "click": click,
                        "cpc": cpc,
                        "acos": acos
                    })
            print(merged_asin_info)
            print("-------------")
            print(merged_keyword_info)
            res0 = []
            res1 = []
            if len(merged_asin_info) > 0:
                res0 = await api1.create_adGroup_Negative_Targeting_by_asin_batch(merged_asin_info, user=self.user)
            if len(merged_keyword_info) > 0:
                res1 = await api1.add_adGroup_negative_keyword_batch(merged_keyword_info, user=self.user)
            res = res0 + res1
            return 200,res
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500,e  # Internal Server Error

    async def auto_campaign_name(self, campaignId, new_name):
        try:
            api1 = GenSP(self.db, self.brand, self.market)
            campaign_info = await api1.list_campaigns_api(campaignId)
            if campaign_info["campaigns"] is not None:
                for item in campaign_info["campaigns"]:
                    campaignId = item['campaignId']
                    name = item['name']
                    e = await api1.update_camapign_name(str(campaignId), name, new_name, self.user)
                    if e:
                        return 400, e
                    else:
                        return 200, e
            else:
                return 404,"Campaign not found"  # Campaign not found
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500,e  # Internal Server Error

    async def create_campaign(self, name, bid,matchType):
        try:
            api = GenSP(self.db, self.brand, self.market)
            today = datetime.today()
            startDate = today.strftime('%Y-%m-%d')
            campaign_id, e = await api.create_camapign(name, startDate,{"placementBidding":[],"strategy":"LEGACY_FOR_SALES"},
                                                         None,None, matchType,
                                           'ENABLED','DAILY', float(bid), self.user)
            if e:
                return 400, None, e
            else:
                return 200, campaign_id, e
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500, None, e  # Internal Server Error

    async def create_adgroup(self, name, bid, campaignId):
        try:
            api = GenSP(self.db, self.brand, self.market)
            adGroupId, e = await api.create_adgroup(campaignId, name, bid,
                                           'ENABLED', self.user)
            if e:
                return 400, None, e
            else:
                return 200, adGroupId, e
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500, None, e  # Internal Server Error

    async def create_sku(self, sku, campaignId,adGroupId):
        try:
            api = GenSP(self.db, self.brand, self.market)
            adId, e = await api.create_productsku(campaignId,adGroupId, sku, None,
                                           'ENABLED', self.user)
            if e:
                return 400, None, e
            else:
                return 200, adId, e
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500, None, e  # Internal Server Error

    async def create_sku_batch(self, skus, campaignIds,adGroupIds):
        try:
            api1 = GenSP(self.db, self.brand, self.market)
            merged_keyword_info = []
            for sku, campaignId, adGroupId in zip(skus, campaignIds, adGroupIds):
                merged_keyword_info.append({
                    "campaignId": campaignId,
                    "adGroupId": adGroupId,
                    "sku": sku  # 从 mapping 中获取 bid_old
                })
            res = await api1.create_productsku_batch(merged_keyword_info, user=self.user)
            return 200,res,None
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500,None,e  # Internal Server Error

    async def list_adGroup_TargetingClause(self, adGroupId):
        try:
            api = GenSP(self.db, self.brand, self.market)
            info = await api.list_adGroup_TargetingClause(adGroupId)
            if "errors" in info and info["errors"]:
                return 400, None, info["errors"][0]["errorType"]
            else:
                return 200, info["targetingClauses"], None
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500, None, e  # Internal Server Error

    async def get_product_api(self, adGroupId):
        try:
            api = GenSP(self.db, self.brand, self.market)
            info = await api.get_product_api(adGroupId)
            if "errors" in info and info["errors"]:
                return 400, None, info["errors"][0]["errorType"]
            else:
                return 200, info["productAds"], None
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500, None, e  # Internal Server Error

    async def list_adGroup_Targetingrecommendations(self, asins):
        try:
            api = GenSP(self.db, self.brand, self.market)
            info = await api.list_adGroup_Targetingrecommendations(asins)
            if "code" in info and info["code"]:
                return 400, None, info["details"]
            else:
                return 200, info, None
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500, None, e  # Internal Server Error

    async def list_category_refinements(self, categoryId):
        try:
            api = GenSP(self.db, self.brand, self.market)
            info = await api.list_category_refinements(categoryId)
            if "code" in info and info["code"]:
                return 400, None, info["details"]
            else:
                return 200, info, None
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500, None, e  # Internal Server Error

    async def list_CampaignNegativeKeywords(self, categoryId):
        try:
            api = GenSP(self.db, self.brand, self.market)
            info = await api.list_Campaign_Negative_Keywords(categoryId)
            if "code" in info and info["code"]:
                return 400, None, info["details"]
            else:
                return 200, info, None
        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 500, None, e  # Internal Server Error

