import json
import os
import asyncio
import pymysql
import pandas as pd

from db.base.db_api import BaseDb


class DbNewSpTools(BaseDb):
    def __init__(self, db, brand, market, log=True):
        super().__init__(db, brand, market, log)

    async def batch_expanded_asin_info(self, updates):
        try:
            async with self.conn.cursor() as cursor:
                for update in updates:
                    # 查询是否已经存在相同的记录
                    query_check = """
                    SELECT COUNT(*) FROM expanded_asin_info 
                    WHERE `classification_id` = %s AND `Asin` = %s AND `Date` = %s
                    """
                    await cursor.execute(query_check, (update['classification_id'], update['Asin'], update['Date']))
                    result = await cursor.fetchone()

                    # 如果不存在，则执行插入操作
                    if result[0] == 0:
                        query_insert = """
                        INSERT INTO expanded_asin_info (`market`, `classification_id`, `Asin`, `Rank`, `Date`) 
                        VALUES (%s, %s, %s, %s, %s)
                        """
                        await cursor.execute(query_insert, (
                        update['market'], update['classification_id'], update['Asin'], update['Rank'], update['Date']))
                await self.conn.commit()
                print("Records inserted successfully into expanded_asin_info table")
        except Exception as e:
            print(f"Error occurred when inserting into expanded_asin_info: {e}")
        finally:
            # 确保连接关闭
            await self.close_connection()

    async def update_sp_campaign(self,market,campaign_name,campaign_id,change_type,budget_old,budget_new,standards_acos,acos,beizhu,status,update_time,user='test'):
        try:
            query = "INSERT INTO amazon_campaign_update (market, campaign_name, campaign_id,change_type, old_value, new_value, standards_acos, acos, beizhu, status, update_time,user) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (market, campaign_name, campaign_id,change_type, budget_old, budget_new, standards_acos, acos, beizhu, status,update_time,user)
            async with self.conn.cursor() as cursor:
                await cursor.execute(query, values)
            await self.conn.commit()
            print("Record inserted successfully into amazon_campaign_update table")
        except Exception as e:
            print(f"Error occurred: {e}")

    async def batch_update_sp_campaign(self,updates):
        try:
            query = "INSERT INTO amazon_campaign_update (market, campaign_name, campaign_id,change_type, old_value, new_value, standards_acos, acos, beizhu, status, update_time,user) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            async with self.conn.cursor() as cursor:
            # 批量执行插入
                await cursor.executemany(query, [(update['market'], update['campaign_name'], update['campaign_id'], update['change_type'],
                                            update['budget_old'], update['budget_new'], update['standards_acos'], update['acos'], update['beizhu'],
                                                  update['status'], update['update_time'], update['user']) for
                                           update in updates])

            await self.conn.commit()
            print("Record inserted successfully into amazon_campaign_update table")
        except Exception as e:
            print(f"Error occurred: {e}")

    # 新建广告活动
    async def create_sp_campaigin(self,market,portfolioId,endDate,campaign_name,campaign_id,targetingType,state,startDate,budgetType,budget,operation_state,create_time,campaign_type,costType,user='test'):
        try:
            query = "INSERT INTO amazon_campaign_create (market,portfolioId,endDate,campaign_name,campaign_id,targetingType,state,startDate,budgetType,budget,operation_state,create_time,campaign_type,costType,user) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (market,portfolioId,endDate,campaign_name,campaign_id,targetingType,state,startDate,budgetType,budget,operation_state,create_time,campaign_type,costType,user)
            async with self.conn.cursor() as cursor:
                await cursor.execute(query, values)
            await self.conn.commit()
            print("Record inserted successfully into create_sp_campaigin table")
        except Exception as e:
            print(f"Error occurred when into create_sp_campaigin: {e}")

    # 新建广告组
    async def create_sp_adgroups(self,market,campaignId,adGroupName,adGroupId,state,defaultBid,beizhu,adGroupState,update_time,creativeType,adGroupType,user='test'):
        try:
            query = "INSERT INTO amazon_adgroups_create (market,campaignId,adGroupName,adGroupId,state,defaultBid,beizhu,adGroupState,update_time,creativeType,adGroupType,user) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (market,campaignId,adGroupName,adGroupId,state,defaultBid,beizhu,adGroupState,update_time,creativeType,adGroupType,user)
            async with self.conn.cursor() as cursor:
                await cursor.execute(query, values)
            await self.conn.commit()
            print("Record inserted successfully into amazon_adgroups_create table")
        except Exception as e:
            print(f"Error occurred when into amazon_adgroups_create table: {e}")

    async def update_sp_adgroups(self,market,adGroupName,adGroupId,bid_old,bid_new,standards_acos,acos,beizhu,status,update_time,user='test'):
        try:
            query = "INSERT INTO amazon_adgroups_update (market, adGroupName, adGroupId, bid_old, bid_new, standards_acos, acos, beizhu, status, update_time,user) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (market,adGroupName,adGroupId,bid_old,bid_new, standards_acos, acos, beizhu, status,update_time,user)
            async with self.conn.cursor() as cursor:
                await cursor.execute(query, values)
            await self.conn.commit()
            print("Record inserted successfully into amazon_adgroups_update table")
        except Exception as e:
            print(f"Error occurred: {e}")

    # 对应新增品的记录log
    async def create_sp_product(self,market,campaignId,asin,sku,adGroupId,adId,status,update_time,productType,user='test'):
        try:
            query = "INSERT INTO amazon_product_create (market, campaignId, asin, sku, adGroupId, adId,status, update_time,productType,user) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (market,campaignId,asin,sku,adGroupId, str(adId), status,update_time,productType,user)
            async with self.conn.cursor() as cursor:
                await cursor.execute(query, values)
            await self.conn.commit()
            print("Record inserted successfully into amazon_product_create table")
        except Exception as e:
            print(f"Error occurred when into amazon_product_create: {e}")

    async def batch_create_sp_product(self,updates):
        try:
            query = "INSERT INTO amazon_product_create (market, campaignId, asin, sku, adGroupId, adId,status, update_time,productType,user) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            async with self.conn.cursor() as cursor:
                # 批量执行插入
                await cursor.executemany(query, [
                    (update['market'], update['campaignId'], update['asin'], update['sku'],
                     update['adGroupId'], update['adId'], update['status'], update['update_time'],
                     update['productType'], update['user']) for
                    update in updates])
            await self.conn.commit()
            print("Record inserted successfully into amazon_product_create table")
        except Exception as e:
            print(f"Error occurred when into amazon_product_create: {e}")

    # 对应修改品的记录log
    async def update_sp_product(self, market, adId, state_new,status, update_time,user='test',campaignId=None,campaignName=None,click=None,cpc=None,acos=None):
        try:
            query = "INSERT INTO amazon_product_update (market, adId, state_new, status, update_time,user,campaignId,campaignName,click,cpc,acos) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (market, adId, state_new, status, update_time,user,campaignId,campaignName,click,cpc,acos)
            async with self.conn.cursor() as cursor:
                await cursor.execute(query, values)
            await self.conn.commit()
            print("Record inserted successfully into amazon_product_update table")
        except Exception as e:
            print(f"Error occurred when into amazon_product_update: {e}")

    async def batch_update_sp_product(self, updates):
        try:
            query = "INSERT INTO amazon_product_update (market, adId, state_new, status, update_time,user,campaignId,campaignName,click,cpc,acos) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            async with self.conn.cursor() as cursor:
                # 批量执行插入
                await cursor.executemany(query, [
                    (update['market'], update['adId'], update['state_new'], update['status'],
                     update['update_time'], update['user'], update['campaignId'], update['campaignName'],
                     update['click'], update['cpc'], update['acos']) for
                    update in updates])
            await self.conn.commit()
            print("Record inserted successfully into amazon_product_update table")
        except Exception as e:
            print(f"Error occurred when into amazon_product_update: {e}")

    # sp广告组新增关键词
    async def add_sp_keyword_toadGroup(self,market,keywordId,campaignId,matchType,state,bid,adGroupId,keywordText,keywordText_new,operation_state,create_time,user='test'):
        try:
            query = "INSERT INTO amazon_keyword_create (market,keywordId,campaignId,matchType,state,bid,adGroupId,keywordText_old,keywordText_new,operation_state,create_time,user) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (market,keywordId,campaignId,matchType,state,bid,adGroupId,keywordText,keywordText_new,operation_state,create_time,user)
            async with self.conn.cursor() as cursor:
                await cursor.execute(query, values)
            await self.conn.commit()
            print("Record inserted successfully into amazon_keyword_create table")
        except Exception as e:
            print(f"Error occurred when into amazon_keyword_create: {e}")

    async def batch_add_sp_keyword_toadGroup(self,updates):
        try:
            query = "INSERT INTO amazon_keyword_create (market,keywordId,campaignId,matchType,state,bid,adGroupId,keywordText_old,keywordText_new,operation_state,create_time,user) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            async with self.conn.cursor() as cursor:
            # 批量执行插入
                await cursor.executemany(query, [(update['market'], update['keywordId'], update['campaignId'], update['matchType'],
                                            update['state'], update['bid'], update['adGroupId'], update['keywordText'], update['keywordText_new'],
                                            update['operation_state'], update['create_time'], update['user']) for
                                           update in updates])

            await self.conn.commit()
            print("Record inserted successfully into amazon_keyword_create table")
        except Exception as e:
            print(f"Error occurred when into amazon_keyword_create: {e}")

    # sp广告组关键词调整
    async def update_sp_keyword_toadGroup(self,market,keywordId,state,bid_old,bid_new,operation_state,create_time,user='test'):
        try:
            query = "INSERT INTO amazon_keyword_update (market,keywordId,state,bid_old,bid_new,operation_state,create_time,user) VALUES (%s,%s, %s, %s, %s, %s, %s, %s)"
            values = (market,keywordId,state,bid_old,bid_new,operation_state,create_time,user)
            async with self.conn.cursor() as cursor:
                await cursor.execute(query, values)
            await self.conn.commit()
            print("Record inserted successfully into update_sp_keyword_toadGroup table")
        except Exception as e:
            print(f"Error occurred when into update_sp_keyword_toadGroup: {e}")

    async def batch_update_sp_keywords(self, updates):
        try:
            # 创建插入的 SQL 语句
            query = "INSERT INTO amazon_keyword_update (market, keywordId, state, bid_old, bid_new, operation_state, create_time, user) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

            async with self.conn.cursor() as cursor:
            # 批量执行插入
                await cursor.executemany(query, [(update['market'], update['keywordId'], update['state'], update['bid_old'],
                                            update['bid_new'], update['operation_state'], update['create_time'], update['user']) for
                                           update in updates])

            await self.conn.commit()
            print("Records inserted successfully into update_sp_keyword_toadGroup table")
        except Exception as e:
            print(f"Error occurred while inserting into update_sp_keyword_toadGroup: {e}")

    # sp广告系列的placement更新
    async def update_sp_campaign_placement(self,market,campaignId,placement,percentage_old,percentage_new,beizhu,status,update_time,user='test'):
        try:
            query = "INSERT INTO amazon_campaign_placement_update (market,campaignId,placement,percentage_old,percentage_new,beizhu,status,update_time,user) VALUES (%s,%s, %s, %s, %s, %s, %s, %s)"
            values = (market,campaignId,placement,percentage_old,percentage_new,beizhu,status,update_time,user)
            async with self.conn.cursor() as cursor:
                await cursor.execute(query, values)
            await self.conn.commit()
            print("Record inserted successfully into amazon_campaign_placement_update table")
        except Exception as e:
            print(f"Error occurred when into amazon_campaign_placement_update: {e}")


    # sp广告系列新增negativeKeyword
    async def add_sp_campaign_negativeKeyword(self,market,adGroupName,adGroupId,campaignId,campaignName,matchType,keyword_state,keywordText,keywordText_new,campaignNegativeKeywordId,operation_state,update_time,user='test'):
        try:
            query = "INSERT INTO amazon_negative_keyword_create (market,adGroupName,adGroupId,campaignId,campaignName,matchType,keyword_state,keywordText,keywordText_new,campaignNegativeKeywordId,operation,operation_state,update_time,user) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s,%s, 'campaign_add', %s, %s, %s)"
            values = (market,adGroupName,adGroupId,campaignId,campaignName,matchType,keyword_state,keywordText,keywordText_new,campaignNegativeKeywordId,operation_state,update_time,user)
            async with self.conn.cursor() as cursor:
                await cursor.execute(query, values)
            await self.conn.commit()
            print("Record inserted successfully into amazon_negative_keyword_create table")
        except Exception as e:
            print(f"Error occurred when into amazon_negative_keyword_create: {e}")

    # sp广告系列更改negativeKeyword
    async def update_sp_campaign_negativeKeyword(self, market,keyword_state, keywordText, campaignNegativeKeywordId, operation_state,update_time,user='test'):
        try:
            query = "INSERT INTO amazon_negative_keyword_update (market,keyword_state,keywordText,campaignNegativeKeywordId,operation,operation_state,update_time,user) VALUES (%s,%s, %s, %s, 'campaign_update', %s, %s, %s)"
            values = (market,keyword_state,keywordText,campaignNegativeKeywordId,operation_state,update_time,user)
            async with self.conn.cursor() as cursor:
                await cursor.execute(query, values)
            await self.conn.commit()
            print("Record inserted successfully into amazon_negative_keyword_update table")
        except Exception as e:
            print(f"Error occurred when into amazon_negative_keyword_update: {e}")

    # sp广告组新增negativeKeyword
    async def add_sp_adGroup_negativeKeyword(self, market, adGroupName, adGroupId, campaignId, campaignName, matchType,
                                        keyword_state, keywordText, operation_state,
                                        update_time,campaignNegativeKeywordId,keywordText_new,user='test'):
        try:
            query = "INSERT INTO amazon_negative_keyword_create (market,adGroupName,adGroupId,campaignId,campaignName,matchType,keyword_state,keywordText,operation,operation_state,update_time,campaignNegativeKeywordId,keywordText_new,user) VALUES (%s, %s, %s, %s, %s,%s, %s,%s, 'addGroup_add', %s, %s, %s, %s, %s)"
            values = (market, adGroupName, adGroupId, campaignId, campaignName, matchType, keyword_state, keywordText, operation_state, update_time,campaignNegativeKeywordId,keywordText_new,user)
            async with self.conn.cursor() as cursor:
                await cursor.execute(query, values)
            await self.conn.commit()
            print("Record inserted successfully into amazon_negative_keyword_create table")
        except Exception as e:
            print(f"Error occurred when into amazon_negative_keyword_create: {e}")

    async def batch_add_sp_adGroup_negativeKeyword(self, updates):
        try:
            query = "INSERT INTO amazon_negative_keyword_create (market,adGroupName,adGroupId,campaignId,campaignName,matchType,keyword_state,keywordText,operation,operation_state,update_time,campaignNegativeKeywordId,keywordText_new,user,click,cpc,acos) VALUES (%s, %s, %s, %s, %s,%s, %s,%s, 'addGroup_add', %s, %s, %s, %s, %s, %s, %s, %s)"
            async with self.conn.cursor() as cursor:
                await cursor.executemany(query, [(update['market'], update['adGroupName'], update['adGroupId'], update['campaignId'],update['campaignName'],
                                        update['matchType'], update['keyword_state'], update['keywordText'],update['operation_state'],update['update_time'],
                                        update['campaignNegativeKeywordId'],update['keywordText_new'],update['user'],update['click'],update['cpc'],update['acos'])
                                       for
                                       update in updates])

            await self.conn.commit()
            print("Record inserted successfully into amazon_negative_keyword_create table")
        except Exception as e:
            print(f"Error occurred when into amazon_negative_keyword_create: {e}")

    # sp广告组更改negativeKeyword
    async def update_sp_adGroup_negativeKeyword(self, market, keyword_state, keywordText, campaignNegativeKeywordId,
                                           operation_state, update_time,user='test'):
        try:
            query = "INSERT INTO amazon_negative_keyword_update (market,keyword_state,keywordText,campaignNegativeKeywordId,operation,operation_state,update_time,user) VALUES (%s,%s, %s, %s, 'adGroup_update', %s, %s, %s)"
            values = (market, keyword_state, keywordText, campaignNegativeKeywordId, operation_state, update_time,user)
            async with self.conn.cursor() as cursor:
                await cursor.execute(query, values)
            await self.conn.commit()
            print("Record inserted successfully into amazon_negative_keyword_update table")
        except Exception as e:
            print(f"Error occurred when into amazon_negative_keyword_update: {e}")

    async def batch_update_sp_adGroup_negativeKeyword(self, updates):
        try:
            query = "INSERT INTO amazon_negative_keyword_update (market,keyword_state,keywordText,campaignNegativeKeywordId,operation,operation_state,update_time,user) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            async with self.conn.cursor() as cursor:
                await cursor.executemany(query, [(update['market'], update['keyword_state'], update['keywordText'],
                                        update['campaignNegativeKeywordId'], update['operation'],
                                        update['operation_state'], update['update_time'], update['user'])
                                       for
                                       update in updates])

            await self.conn.commit()
            print("Record inserted successfully into amazon_negative_keyword_update table")
        except Exception as e:
            print(f"Error occurred when into amazon_negative_keyword_update: {e}")

    async def add_sd_adGroup_Targeting(self, market,adGroupId,bid,expression_type,state,expression,targetingType,targetingState, update_time,targetId,user='test',campaignId = None):
        try:
            query = "INSERT INTO amazon_targeting_create (market,adGroupId,bid,expressionType,state,expression,targetingType,targetingState,update_time,user,targetId,campaignId) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (market,adGroupId,bid,expression_type,state,expression,targetingType,targetingState, update_time,user,targetId,campaignId)
            async with self.conn.cursor() as cursor:
                await cursor.execute(query, values)
            await self.conn.commit()
            print("Record inserted successfully into amazon_targeting_create table")
        except Exception as e:
            print(f"Error occurred when into amazon_targeting_create: {e}")


    async def batch_add_sd_adGroup_Targeting(self,updates):
        try:
            query = "INSERT INTO amazon_targeting_create (market,adGroupId,bid,expressionType,state,expression,targetingType,targetingState,update_time,user,targetId,campaignId,campaignName,click,cpc,acos) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            async with self.conn.cursor() as cursor:
                await cursor.executemany(query, [(update['market'], update['adGroupId'], update['bid'], update['expressionType'],
                                        update['state'], update['expression'], update['targetingType'],update['targetingState'],update['update_time'],
                                        update['user'],update['targetId'],update['campaignId'],update['campaignName'],update['click'],update['cpc'],update['acos']) for
                                       update in updates])

            await self.conn.commit()
            print("Record inserted successfully into amazon_targeting_create table")
        except Exception as e:
            print(f"Error occurred when into amazon_targeting_create: {e}")


    async def update_sd_adGroup_Targeting(self, market,adGroupId,bid_old,bid,state,expression,targetingType,targetingState, update_time,user='test'):
        try:
            query = "INSERT INTO amazon_targeting_update (market,adGroupId,bid_old,state,expression,targetingType,targetingState,update_time,user,bid_new) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (market,adGroupId,bid_old,state,expression,targetingType,targetingState, update_time,user,bid)
            async with self.conn.cursor() as cursor:
                await cursor.execute(query, values)
            await self.conn.commit()
            print("Record inserted successfully into amazon_targeting_update table")
        except Exception as e:
            print(f"Error occurred when into amazon_targeting_update: {e}")

    async def batch_update_adGroup_Targeting(self, updates):
        try:
            # 创建插入的 SQL 语句
            query = "INSERT INTO amazon_targeting_update (market,adGroupId,bid_old,state,expression,targetingType,targetingState,update_time,user,bid_new) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            # 批量执行插入
            async with self.conn.cursor() as cursor:
                await cursor.executemany(query, [(update['market'], update['adGroupId'], update['bid_old'], update['state'],
                                        update['expression'], update['targetingType'], update['targetingState'],
                                        update['update_time'], update['user'], update['bid_new']) for
                                       update in updates])

            await self.conn.commit()
            print("Records inserted successfully into batch_update_adGroup_Targeting table")
        except Exception as e:
            print(f"Error occurred while inserting into batch_update_adGroup_Targeting: {e}")

    def create_budget_info(self, market, brand, strategy, type1, campaignId, campaignName, Budget, New_Budget,
                           cost_yesterday, clicks_yesterday, ACOS_yesterday, total_clicks_7d, total_sales14d_7d,
                           ACOS_7d, ACOS_30d, total_clicks_30d, total_sales14d_30d, Reason, country_avg_ACOS_1m,
                           bid_adjust, date, create_time, Operational_Status):
        try:
            conn = self.conn
            cursor = conn.cursor()
            # 检查是否存在重复数据
            check_query = """
                                SELECT COUNT(*) FROM budget_info
                                WHERE market = %s AND brand = %s AND strategy = %s AND type = %s AND campaignId = %s AND campaignName = %s
                                AND Reason = %s AND date = %s
                                """
            check_values = (
                market, brand, strategy, type1, campaignId, campaignName, Reason, date
            )
            cursor.execute(check_query, check_values)
            count = cursor.fetchone()[0]
            print(count)
            if count > 0:
                print("数据已存在，跳过插入")
            else:
                # 注意：确保查询中的列顺序与您的表中列的顺序相匹配
                query = """
                INSERT INTO budget_info
                (market, brand, strategy, type, campaignId, campaignName, Budget, New_Budget, cost_yesterday, clicks_yesterday, ACOS_yesterday, total_clicks_7d, total_sales14d_7d, ACOS_7d, ACOS_30d, total_clicks_30d, total_sales14d_30d, Reason, country_avg_ACOS_1m, bid_adjust, date, create_time, Operational_Status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    market, brand, strategy, type1, campaignId, campaignName, Budget, New_Budget, cost_yesterday, clicks_yesterday, ACOS_yesterday, total_clicks_7d, total_sales14d_7d, ACOS_7d, ACOS_30d, total_clicks_30d, total_sales14d_30d, Reason, country_avg_ACOS_1m, bid_adjust, date, create_time, Operational_Status
                )
                cursor.execute(query, values)
                conn.commit()
                table2 = [[market, date, "广告活动预算", campaignName, "","关闭" if bid_adjust == 0 else bid_adjust]]
                get_request_data(market,date,"D-LOG",table2,0,brand)
                print("Record inserted successfully into budget_info table")
        except Exception as e:
            print(f"Error occurred when inserting into budget_info: {e}")

    def create_sku_info(self, market, brand, strategy, type1, campaignName, adGroupName, adId, ACOS_30d,
                        total_clicks_30d, total_sales14d_30d, total_cost_30d, ACOS_7d, total_clicks_7d,
                        total_sales14d_7d, total_cost_7d, advertisedSku, ORDER_1m, Reason, date, create_time, Operational_Status):
        try:
            conn = self.conn
            cursor = conn.cursor()
            # 检查是否存在重复数据
            check_query = """
                                    SELECT COUNT(*) FROM sku_info
                                    WHERE market = %s AND brand = %s AND strategy = %s AND type = %s AND campaignName = %s AND adGroupName = %s
                                    AND adId = %s AND Reason = %s AND date = %s
                                    """
            check_values = (
                market, brand, strategy, type1, campaignName, adGroupName, adId, Reason,
                date
            )
            cursor.execute(check_query, check_values)
            count = cursor.fetchone()[0]
            print(count)
            if count > 0:
                print("数据已存在，跳过插入")
            else:
                # 确保查询中的列顺序与表结构中的列顺序一致
                query = """
                INSERT INTO sku_info
                (market, brand, strategy, type, campaignName, adGroupName, adId, ACOS_30d, total_clicks_30d, total_sales14d_30d, total_cost_30d, ACOS_7d, total_clicks_7d, total_sales14d_7d, total_cost_7d, advertisedSku, ORDER_1m, Reason, date, create_time, Operational_Status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    market, brand, strategy, type1, campaignName, adGroupName, adId, ACOS_30d, total_clicks_30d, total_sales14d_30d, total_cost_30d, ACOS_7d, total_clicks_7d, total_sales14d_7d, total_cost_7d, advertisedSku, ORDER_1m, Reason, date, create_time, Operational_Status
                )
                cursor.execute(query, values)
                conn.commit()
                if type1 == "手动_关闭":
                    sku_status = "关闭"
                elif type1 == "自动_关闭":
                    sku_status = "关闭"
                elif type1 == "手动_复开":
                    sku_status = "复开"
                elif type1 == "自动_复开":
                    sku_status = "复开"
                elif type1 == "SD_关闭":
                    sku_status = "关闭"
                elif type1 == "SD_复开":
                    sku_status = "复开"
                else:
                    sku_status = "关闭"
                table2 = [[market, date, "SKU状态", campaignName, advertisedSku, sku_status]]
                get_request_data(market, date, "D-LOG", table2, 0, brand)
                print("数据成功插入到 sku_info 表中")
        except Exception as e:
            print(f"插入数据到 sku_info 表时出错: {e}")

    def create_campaign_placement_info(self, market, brand, strategy, type1, campaignName, campaignId, placementClassification,
                                       bid, new_bid, ACOS_7d, total_clicks_7d, total_sales14d_7d, ACOS_3d, total_sales14d_3d,
                                       total_cost_3d, reason, bid_adjust, date, create_time, Operational_Status):
        try:
            conn = self.conn
            cursor = conn.cursor()
            # 检查是否存在重复数据
            check_query = """
                        SELECT COUNT(*) FROM campaign_placement_info
                        WHERE market = %s AND brand = %s AND strategy = %s AND type = %s AND campaignName = %s AND campaignId = %s
                        AND placementClassification = %s AND reason = %s AND date = %s
                        """
            check_values = (
                market, brand, strategy, type1, campaignName, campaignId, placementClassification, reason,
                date
            )
            cursor.execute(check_query, check_values)
            count = cursor.fetchone()[0]
            print(count)
            if count > 0:
                print("数据已存在，跳过插入")
            else:
                # 确保查询中的列顺序与表结构中的列顺序一致
                query = """
                INSERT INTO campaign_placement_info
                (market, brand, strategy, type, campaignName, campaignId, placementClassification, bid, new_bid, ACOS_7d, total_clicks_7d, total_sales14d_7d, ACOS_3d, total_sales14d_3d, total_cost_3d, reason, bid_adjust, date, create_time, Operational_Status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    market, brand, strategy, type1, campaignName, campaignId, placementClassification, bid, new_bid, ACOS_7d, total_clicks_7d, total_sales14d_7d, ACOS_3d, total_sales14d_3d, total_cost_3d, reason, bid_adjust, date, create_time, Operational_Status
                )
                cursor.execute(query, values)
                conn.commit()
                table2 = [[market, date, "广告位竞价", campaignName, placementClassification, "将广告位竞价设置为0" if bid_adjust == 0 else bid_adjust]]
                get_request_data(market, date, "D-LOG", table2, 0, brand)
                print("数据成功插入到 campaign_placement_info 表中")
        except Exception as e:
            print(f"插入数据到 campaign_placement_info 表时出错: {e}")

    def create_search_term_info(self, market, brand, strategy, type1, campaignName, campaignId, adGroupName, adGroupId,
                                ACOS_30d, ORDER_1m, total_clicks_30d, total_cost_30d, ACOS_7d, ORDER_7d, total_clicks_7d,
                                total_sales14d_7d, total_cost_7d, searchTerm, select_campaignId, reason, date, create_time, Operational_Status):
        try:
            conn = self.conn
            cursor = conn.cursor()
            # 检查是否存在重复数据
            check_query = """
                            SELECT COUNT(*) FROM search_term_info
                            WHERE market = %s AND brand = %s AND strategy = %s AND type = %s AND campaignName = %s AND campaignId = %s
                            AND adGroupName = %s AND adGroupId = %s AND searchTerm = %s AND reason = %s AND date = %s
                                            """
            check_values = (
                market, brand, strategy, type1, campaignName, campaignId, adGroupName, adGroupId, searchTerm, reason, date
            )
            cursor.execute(check_query, check_values)
            count = cursor.fetchone()[0]
            print(count)
            if count > 0:
                print("数据已存在，跳过插入")
            else:
                # 确保查询中的列顺序与表结构中的列顺序一致
                query = """
                INSERT INTO search_term_info
                (market, brand, strategy, type, campaignName, campaignId, adGroupName, adGroupId, ACOS_30d, ORDER_1m, total_clicks_30d, total_cost_30d, ACOS_7d, ORDER_7d, total_clicks_7d, total_sales14d_7d, total_cost_7d, searchTerm, select_campaignId, reason, date, create_time, Operational_Status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    market, brand, strategy, type1, campaignName, campaignId, adGroupName, adGroupId, ACOS_30d, ORDER_1m, total_clicks_30d, total_cost_30d, ACOS_7d, ORDER_7d, total_clicks_7d, total_sales14d_7d, total_cost_7d, searchTerm, select_campaignId, reason, date, create_time, Operational_Status
                )
                cursor.execute(query, values)
                conn.commit()
                print("数据成功插入到 search_term_info 表中")
        except Exception as e:
            print(f"插入数据到 search_term_info 表时出错: {e}")

    def create_keyword_info(self, market, brand, strategy, type1, keyword, keywordId, campaignName, adGroupName,
                            matchType, keywordBid, new_keywordBid, ACOS_30d, ORDER_1m, total_clicks_30d,
                            total_sales14d_30d, total_cost_30d, ORDER_15d, ACOS_7d, total_clicks_7d, total_sales14d_7d,
                            total_cost_7d, ACOS_3d, total_sales14d_3d, total_cost_3d, reason, bid_adjust, date, create_time,
                            Operational_Status):
        try:
            conn = self.conn
            cursor = conn.cursor()
            # 检查是否存在重复数据
            check_query = """
                                            SELECT COUNT(*) FROM keyword_info
                                            WHERE market = %s AND brand = %s AND strategy = %s AND type = %s AND keyword = %s AND keywordId = %s
                                            AND campaignName = %s AND adGroupName = %s AND matchType = %s AND reason = %s AND date = %s
                                            """
            check_values = (
                market, brand, strategy, type1, keyword, keywordId, campaignName, adGroupName,
                matchType, reason, date
            )
            cursor.execute(check_query, check_values)
            count = cursor.fetchone()[0]
            print(count)
            if count > 0:
                print("数据已存在，跳过插入")
            else:
                # 确保查询中的列顺序与表结构中的列顺序一致
                query = """
                INSERT INTO keyword_info
                (market, brand, strategy, type, keyword, keywordId, campaignName, adGroupName, matchType, keywordBid, new_keywordBid, ACOS_30d, ORDER_1m, total_clicks_30d, total_sales14d_30d, total_cost_30d, ORDER_15d, ACOS_7d, total_clicks_7d, total_sales14d_7d, total_cost_7d, ACOS_3d, total_sales14d_3d, total_cost_3d, reason, bid_adjust, date, create_time, Operational_Status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    market, brand, strategy, type1, keyword, keywordId, campaignName, adGroupName, matchType, keywordBid,
                    new_keywordBid, ACOS_30d, ORDER_1m, total_clicks_30d, total_sales14d_30d, total_cost_30d, ORDER_15d, ACOS_7d,
                    total_clicks_7d, total_sales14d_7d, total_cost_7d, ACOS_3d, total_sales14d_3d, total_cost_3d, reason, bid_adjust,
                    date, create_time, Operational_Status
                )
                cursor.execute(query, values)
                conn.commit()
                if matchType == "BROAD":
                    keyword_type = "关键词_广泛匹配"
                elif matchType == "PHRASE":
                    keyword_type = "关键词_短语匹配"
                elif matchType == "EXACT":
                    keyword_type = "关键词_精准匹配"
                else:
                    keyword_type = "关键词"
                table2 = [[market, date, keyword_type, campaignName, keyword, bid_adjust]]
                get_request_data(market, date, "D-LOG", table2, 0, brand)
                print("数据成功插入到 keyword_info 表中")
        except Exception as e:
            print(f"插入数据到 keyword_info 表时出错: {e}")

    def create_automatic_targeting_info(self, market, brand, strategy, type1, keyword, keywordId, campaignName, adGroupName,
                             keywordBid, new_keywordBid, ACOS_30d, total_clicks_30d,
                            total_sales14d_30d, total_cost_30d, ORDER_15d, ACOS_7d, total_clicks_7d, total_sales14d_7d,
                            total_cost_7d, ACOS_3d, total_sales14d_3d, total_cost_3d, reason, bid_adjust, date, create_time,
                            Operational_Status):
        try:
            conn = self.conn
            cursor = conn.cursor()
            # 检查是否存在重复数据
            check_query = """
                                            SELECT COUNT(*) FROM automatic_targeting_info
                                            WHERE market = %s AND brand = %s AND strategy = %s AND type = %s AND keyword = %s AND keywordId = %s
                                            AND campaignName = %s AND adGroupName = %s AND reason = %s AND date = %s
                                            """
            check_values = (
                market, brand, strategy, type1, keyword, keywordId, campaignName, adGroupName,
                reason, date
            )
            cursor.execute(check_query, check_values)
            count = cursor.fetchone()[0]
            print(count)
            if count > 0:
                print("数据已存在，跳过插入")
            else:
                # 确保查询中的列顺序与表结构中的列顺序一致
                query = """
                INSERT INTO automatic_targeting_info
                (market, brand, strategy, type, keyword, keywordId, campaignName, adGroupName, keywordBid, new_keywordBid, ACOS_30d, total_clicks_30d, total_sales14d_30d, total_cost_30d, ORDER_15d, ACOS_7d, total_clicks_7d, total_sales14d_7d, total_cost_7d, ACOS_3d, total_sales14d_3d, total_cost_3d, reason, bid_adjust, date, create_time, Operational_Status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    market, brand, strategy, type1, keyword, keywordId, campaignName, adGroupName, keywordBid,
                    new_keywordBid, ACOS_30d, total_clicks_30d, total_sales14d_30d, total_cost_30d, ORDER_15d, ACOS_7d,
                    total_clicks_7d, total_sales14d_7d, total_cost_7d, ACOS_3d, total_sales14d_3d, total_cost_3d, reason, bid_adjust,
                    date, create_time, Operational_Status
                )
                cursor.execute(query, values)
                conn.commit()
                table2 = [[market, date, "自动定位组竞价", campaignName, keyword, bid_adjust]]
                get_request_data(market, date, "D-LOG", table2, 0, brand)
                print("数据成功插入到 automatic_targeting_info 表中")
        except Exception as e:
            print(f"插入数据到 automatic_targeting_info 表时出错: {e}")

    def create_product_targets_info(self, market, brand, strategy, type1, keyword, keywordId, campaignName, adGroupName,
                            matchType, keywordBid, new_keywordBid, ACOS_30d, ORDER_1m, total_clicks_30d,
                            total_sales14d_30d, total_cost_30d, ORDER_15d, ACOS_7d, total_clicks_7d, total_sales14d_7d,
                            total_cost_7d, ACOS_3d, total_sales14d_3d, total_cost_3d, reason, bid_adjust, date, create_time,
                            Operational_Status):
        try:
            conn = self.conn
            cursor = conn.cursor()
            # 检查是否存在重复数据
            check_query = """
                                SELECT COUNT(*) FROM product_targets_info
                                WHERE market = %s AND brand = %s AND strategy = %s AND type = %s AND keyword = %s AND keywordId = %s
                                AND campaignName = %s AND adGroupName = %s AND matchType = %s AND reason = %s AND date = %s
                                """
            check_values = (
                market, brand, strategy, type1, keyword, keywordId, campaignName, adGroupName,
                            matchType, reason, date
            )
            cursor.execute(check_query, check_values)
            count = cursor.fetchone()[0]
            print(count)
            if count > 0:
                print("数据已存在，跳过插入")
            else:
                # 确保查询中的列顺序与表结构中的列顺序一致
                query = """
                INSERT INTO product_targets_info
                (market, brand, strategy, type, keyword, keywordId, campaignName, adGroupName, matchType, keywordBid, New_keywordBid,
                 ACOS_30d, ORDER_1m, total_clicks_30d, total_sales14d_30d, total_cost_30d, ORDER_15d, ACOS_7d, total_clicks_7d,
                 total_sales14d_7d, total_cost_7d, ACOS_3d, total_sales14d_3d, total_cost_3d, reason, bid_adjust, date, create_time,
                 Operational_Status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                values = (
                    market, brand, strategy, type1, keyword, keywordId, campaignName, adGroupName, matchType, keywordBid,
                    new_keywordBid, ACOS_30d, ORDER_1m, total_clicks_30d, total_sales14d_30d, total_cost_30d, ORDER_15d, ACOS_7d,
                    total_clicks_7d, total_sales14d_7d, total_cost_7d, ACOS_3d, total_sales14d_3d, total_cost_3d, reason, bid_adjust,
                    date, create_time, Operational_Status
                )

                cursor.execute(query, values)
                conn.commit()
                table2 = [[market, date, "商品投放竞价", campaignName, keyword, bid_adjust]]
                get_request_data(market, date, "D-LOG", table2, 0, brand)
                print("数据成功插入到 product_targets_info 表中")

        except Exception as e:
            print(f"插入数据到 product_targets_info 表时出错: {e}")

    def create_product_targets_search_term_info(self, market, brand, strategy, type1, campaignName, campaignId, adGroupName, adGroupId,
                            ACOS_30d, ORDER_1m, total_clicks_30d, total_cost_30d, ACOS_7d, ORDER_7d, total_clicks_7d,
                            total_sales14d_7d, total_cost_7d, searchTerm, reason, date, create_time, Operational_Status):
        try:
            conn = self.conn
            cursor = conn.cursor()
            # 检查是否存在重复数据
            check_query = """
                    SELECT COUNT(*) FROM product_targets_search_term_info
                    WHERE market = %s AND brand = %s AND strategy = %s AND type = %s AND campaignName = %s AND campaignId = %s
                    AND adGroupName = %s AND adGroupId = %s AND searchTerm = %s AND reason = %s AND date = %s
                    """
            check_values = (
                market, brand, strategy, type1, campaignName, campaignId, adGroupName, adGroupId,
                searchTerm, reason, date
            )
            cursor.execute(check_query, check_values)
            count = cursor.fetchone()[0]
            print(count)
            if count > 0:
                print("数据已存在，跳过插入")
            else:
                # 确保查询中的列顺序与表结构中的列顺序一致
                query = """
                INSERT INTO product_targets_search_term_info
                (market, brand, strategy, type, campaignName, campaignId, adGroupName, adGroupId, ACOS_30d, ORDER_1m,
                 total_clicks_30d, total_cost_30d, ACOS_7d, ORDER_7d, total_clicks_7d, total_sales14d_7d, total_cost_7d,
                 searchTerm, reason, date, create_time, Operational_Status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    market, brand, strategy, type1, campaignName, campaignId, adGroupName, adGroupId, ACOS_30d, ORDER_1m,
                    total_clicks_30d, total_cost_30d, ACOS_7d, ORDER_7d, total_clicks_7d, total_sales14d_7d, total_cost_7d,
                    searchTerm, reason, date, create_time, Operational_Status
                )
                cursor.execute(query, values)
                conn.commit()
                print("数据成功插入到 product_targets_search_term_info 表中")
        except Exception as e:
            print(f"插入数据到 product_targets_search_term_info 表时出错: {e}")

    def create_category_info(self, market, category, category_id):
        try:
            conn = self.conn
            cursor = conn.cursor()
            query = "INSERT INTO category_info (category,category_id,market) VALUES (%s,%s,%s)"
            values = (category, category_id, market)
            cursor.execute(query, values)
            conn.commit()
            print("Record inserted successfully into category_info table")
        except Exception as e:
            print(f"Error occurred when into category_info: {e}")

