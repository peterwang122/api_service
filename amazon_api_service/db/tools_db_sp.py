import json
import os
from datetime import datetime
import aiomysql
import pandas as pd
import pymysql
from db.base.db_api import BaseDb



def get_timestamp():
    # 获取当前时间
    current_time = datetime.now()
    timestamp = int(current_time.timestamp())
    date_string = current_time.strftime("%Y-%m-%d")
    # 组合日期和时间戳
    date_timestamp_string = f"{date_string}_{timestamp}"
    return date_timestamp_string

class DbSpTools(BaseDb):
    def __init__(self, db, brand, market):
        super().__init__(db, brand, market)

    async def get_profileId(self, market):
        # 低于 平均ACOS值 30% 以上的 campaign 广告活动
        # 建议执行的操作：预算提升30%
        try:
            # 确保数据库连接已初始化
            if self.conn is None:
                await self.init()  # 初始化连接
            conn = self.conn
            # 使用异步游标执行 SQL 查询
            query = f"""
SELECT DISTINCT profileId, region FROM amazon_profile
WHERE countryCode = '{market}' AND type = 'seller'
"""
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query)
                result = await cursor.fetchall()
            if result:
                df = pd.DataFrame(result)
                print("get_profileId Data successfully!")
                return df.loc[0, 'profileId'], df.loc[0, 'region']
            else:
                return None, None  # 如果没有结果返回空
        except Exception as error:
            print("get_profileId Error while querying data:", error)
            return None, None

    async def get_classification_id(self, market):
        # 低于 平均ACOS值 30% 以上的 campaign 广告活动
        # 建议执行的操作：预算提升30%
        try:
            # 确保数据库连接已初始化
            if self.conn is None:
                await self.init()  # 初始化连接
            conn = self.conn
            # 使用异步游标执行 SQL 查询
            query = f"""
WITH A AS (
    SELECT
        CASE
            WHEN info_ext.parent_asins = ""
                OR info_ext.parent_asins IS NULL THEN info_ext.asin
            ELSE info_ext.parent_asins
        END AS parent_asins,
        info_ext.classification_rank_classification_id,
        info_ext.classification_rank_title,
        product_sp.campaignId AS campaignId,
        b.campaign_name AS campaignName,
        product_sp.adGroupId AS adGroupId,
        product_sp.market AS market
    FROM
        amazon_sp_productads_list AS product_sp
        LEFT JOIN amazon_product_info_extended AS info_ext
            ON info_ext.asin = product_sp.asin
            AND info_ext.market = product_sp.market
        LEFT JOIN amazon_campaigns_list_sp b
            ON b.campaignId = product_sp.campaignId
        LEFT JOIN amazon_adgroups_list_sp c
            ON c.adgroupId = product_sp.adGroupId
    WHERE
        info_ext.market = '{market}'
        AND product_sp.market = '{market}'
        AND b.state = 'ENABLED'
        AND product_sp.state IN ('ENABLED', 'PAUSED')
        AND c.state = 'ENABLED'
        AND b.campaign_name LIKE '%DeepBI%'
        AND b.campaign_name LIKE '%0514%'
        AND classification_rank_classification_id IS NOT NULL
        AND classification_rank_classification_id != ''
    GROUP BY
        parent_asins,
        product_sp.campaignId
    ORDER BY
        parent_asins
)
SELECT DISTINCT classification_rank_classification_id FROM A
            """
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query)
                result = await cursor.fetchall()
            if result:
                df = pd.DataFrame(result)
                print("get_profileId Data successfully!")
                return df['classification_rank_classification_id'].tolist()
            else:
                return None
        except Exception as error:
            print("get_profileId Error while querying data:", error)
            return None

    async def get_classification_title(self, market):
        # 低于 平均ACOS值 30% 以上的 campaign 广告活动
        # 建议执行的操作：预算提升30%
        try:
            # 确保数据库连接已初始化
            if self.conn is None:
                await self.init()  # 初始化连接
            conn = self.conn
            # 使用异步游标执行 SQL 查询
            query = f"""
    SELECT
        CASE
            WHEN info_ext.parent_asins = ""
                OR info_ext.parent_asins IS NULL THEN info_ext.asin
            ELSE info_ext.parent_asins
        END AS parent_asins,
        info_ext.classification_rank_classification_id,
        info_ext.classification_rank_title,
        product_sp.campaignId AS campaignId,
        b.campaign_name AS campaignName,
        product_sp.adGroupId AS adGroupId,
        product_sp.market AS market
    FROM
        amazon_sp_productads_list AS product_sp
        LEFT JOIN amazon_product_info_extended AS info_ext
            ON info_ext.asin = product_sp.asin
            AND info_ext.market = product_sp.market
        LEFT JOIN amazon_campaigns_list_sp b
            ON b.campaignId = product_sp.campaignId
        LEFT JOIN amazon_adgroups_list_sp c
            ON c.adgroupId = product_sp.adGroupId
    WHERE
        info_ext.market = '{market}'
        AND product_sp.market = '{market}'
        AND b.state = 'ENABLED'
        AND product_sp.state IN ('ENABLED', 'PAUSED')
        AND c.state = 'ENABLED'
        AND b.campaign_name LIKE '%DeepBI%'
        AND b.campaign_name LIKE '%0514%'
#         AND classification_rank_classification_id IS NOT NULL
#         AND classification_rank_classification_id != ''
    GROUP BY
        parent_asins,
        product_sp.campaignId
    ORDER BY
        parent_asins
            """
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query)
                result = await cursor.fetchall()
            if result:
                df = pd.DataFrame(result)
                print("get_profileId Data successfully!")
                return df
            else:
                return None
        except Exception as error:
            print("get_profileId Error while querying data:", error)
            return None

    async def get_serachterm(self, market,parent_asin,day,order):
        # 低于 平均ACOS值 30% 以上的 campaign 广告活动
        # 建议执行的操作：预算提升30%
        try:
            # 确保数据库连接已初始化
            if self.conn is None:
                await self.init()  # 初始化连接
            conn = self.conn
            # 使用异步游标执行 SQL 查询
            query = f"""
WITH a AS (
	SELECT DISTINCT adGroupId 
	FROM 
	amazon_product_info_extended a 
	LEFT JOIN 
	amazon_sp_productads_list b ON a.asin = b.asin AND a.market = b.market
	WHERE 
	parent_asins = '{parent_asin}'
	),
	b AS (
    SELECT
        b.searchTerm,
        SUM(CASE WHEN date BETWEEN DATE_SUB(CURRENT_DATE , INTERVAL {int(day)} day) AND DATE_SUB(CURRENT_DATE, INTERVAL 1 DAY) THEN purchases7d ELSE 0 END) AS ORDER_1m
    FROM
        amazon_search_term_reports_sp b
    JOIN
        a ON b.adGroupId = a.adGroupId
    WHERE
        b.date BETWEEN DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY) AND CURRENT_DATE - INTERVAL 1 DAY
        AND b.market = '{market}'
        AND NOT (b.searchTerm LIKE 'b0%' AND LENGTH(b.searchTerm) = 10) -- 添加排除条件
    GROUP BY
        b.searchTerm
)
SELECT DISTINCT searchTerm FROM b
WHERE 
 b.ORDER_1m >= {int(order)}
            """
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query)
                result = await cursor.fetchall()
            if result:
                df = pd.DataFrame(result)
                print("get_profileId Data successfully!")
                return df['searchTerm'].tolist()
            else:
                return []
        except Exception as error:
            print("get_profileId Error while querying data:", error)
            return []

    def select_sd_campaign_name(self,product):
        try:
            conn = self.conn

            query = """SELECT campaignName FROM amazon_campaign_reports_sd
            WHERE market = '{}'
            AND LOWER(campaignName) LIKE LOWER('%{}%')""".format(self.market, product)
            df = pd.read_sql(query, con=conn)
            if df.empty:
                print("No campaign name")
                return ["faile"]
            else:
                print("campaignName is already exist")
                return ["success"]
        except Exception as e:
            print(f"Error occurred when select_sd_campaign_name: {e}")

    def select_sp_campaign_name(self,product):
        try:
            conn = self.conn

            query = """SELECT campaignName FROM amazon_campaign_reports_sp
            WHERE market = '{}'
            AND LOWER(campaignName) LIKE LOWER('%{}%')""".format(self.market, product)
            df = pd.read_sql(query, con=conn)
            if df.empty:
                print("No campaign name")
                return ["faile"]
            else:
                print("campaignName is already exist")
                return ["success"]
        except Exception as e:
            print(f"Error occurred when select_sd_campaign_name: {e}")

    def select_sd_product_sku(self,product):
        try:
            conn = self.conn
            if self.market in ('US', 'JP', 'UK'):
                sku = f"{self.market.lower()}sku"
            else:
                sku = "frsku"
            query = """
            SELECT {}
FROM prod_as_product_base
WHERE sspu = '{}'
and base_market = 'US'
GROUP BY {}
            """.format(sku, product, sku)
            df = pd.read_sql(query, con=conn)
            if df.empty:
                print("No product sku")
            else:
                print("select sd product sku success")
                return df[sku].tolist()
        except Exception as e:
            print(f"Error occurred when select_sd_product_sku: {e}")

    def select_sp_product_asin(self, market1,market2,asin):
        try:
            conn = self.conn
            asin1 = f"{market1.lower()}asin"
            asin2 = f"{market2.lower()}asin"
            query = """
           SELECT {}
    FROM prod_as_product_base
    WHERE {} = '{}'
            """.format(asin1, asin2, asin)
            df = pd.read_sql(query, con=conn)
            isales = df.loc[0, asin1]
            return isales
        except Exception as e:
            print(f"Error occurred when select_sd_product_sku: {e}")

    def select_sp_product_sku(self, market1,market2,advertisedSku):
        try:
            conn = self.conn
            market1_sku = "frsku"
            market2_sku = f"{market2.lower()}sku"
            query = """
            SELECT {} FROM prod_as_product_base
WHERE base_market = 'US'
and nsspu = (
SELECT nsspu FROM prod_as_product_base
WHERE  base_market = 'US'
and {} = '{}'
GROUP BY nsspu
)
GROUP BY {}
            """.format(market1_sku, market2_sku, advertisedSku,market1_sku)
            df = pd.read_sql(query, con=conn)
            if df.empty:
                print("No product sku")
            else:
                print("select sp product sku success")
                return df[market1_sku].tolist()
        except Exception as e:
            print(f"Error occurred when select_sp_product_sku: {e}")

    def select_product_sku(self, market1,market2,advertisedSku):
        try:
            conn = self.conn
            market1_sku = f"{market1.lower()}sku"
            market2_sku = f"{market2.lower()}sku"
            query = """
            SELECT {} FROM prod_as_product_base
WHERE base_market = 'US'
and nsspu in (
SELECT nsspu FROM prod_as_product_base
WHERE  base_market = 'US'
and {} in %(column1_values1)s
GROUP BY nsspu
)
GROUP BY {}
            """.format(market1_sku, market2_sku,market1_sku)
            df = pd.read_sql(query, con=conn, params={'column1_values1': advertisedSku})
            if df.empty:
                print("No product sku")
            else:
                print("select sp product sku success")
                return df[market1_sku].tolist()
        except Exception as e:
            print(f"Error occurred when select_product_sku: {e}")

    def select_product_sku_by_asin(self, market1,market2,advertisedSku,depository):
        try:
            conn = self.conn
            query1 = f"""
    SELECT
		amazon_product_info_extended.parent_asins AS nsspu
	FROM
		amazon_product_info
		LEFT JOIN amazon_product_info_extended ON amazon_product_info_extended.asin = amazon_product_info.asin
	WHERE
		amazon_product_info.market = '{market2}'
		AND amazon_product_info_extended.market = '{depository}'
	AND amazon_product_info.sku IN %(column1_values1)s
            """
            df1 = pd.read_sql(query1, con=conn, params={'column1_values1': advertisedSku})
            if df1.empty or (df1['nsspu'].str.strip() == '').all():
                print("No product")
                return advertisedSku
            column1_values2 = df1['nsspu'].tolist()
            query2 = f"""
SELECT DISTINCT
	amazon_product_info.sku
FROM
	amazon_product_info
	LEFT JOIN amazon_product_info_extended ON amazon_product_info_extended.asin = amazon_product_info.asin
WHERE
	amazon_product_info.market = '{depository}'
	AND amazon_product_info_extended.market = '{depository}'
	AND amazon_product_info_extended.parent_asins IN %(column1_values2)s
            """
            df = pd.read_sql(query2, con=conn, params={'column1_values2': column1_values2})
            if df.empty:
                print("No product sku")
            else:
                print("select product sku success")
                return df['sku'].tolist()
        except Exception as e:
            print(f"Error occurred when select_product_sku_by_asin: {e}")

    def select_product_sku_by_parent_asin(self, parent_asins, depository):
        try:
            conn = self.conn
            query = f"""
            SELECT DISTINCT
	amazon_product_info.sku
FROM
	amazon_product_info
	LEFT JOIN amazon_product_info_extended ON amazon_product_info_extended.asin = amazon_product_info.asin
WHERE
	amazon_product_info.market = '{depository}'
	AND amazon_product_info_extended.market = '{depository}'
	AND amazon_product_info_extended.parent_asins = '{parent_asins}'
            """
            df = pd.read_sql(query, con=conn)
            if df.empty:
                query1 = f"""
                            SELECT DISTINCT sku
                            FROM amazon_product_info
                            WHERE asin = '{parent_asins}'
                            AND market = '{self.market}'
                            """
                df1 = pd.read_sql(query1, con=conn)
                return df1['sku'].tolist()
            else:
                print("select product sku success")
                return df['sku'].tolist()
        except Exception as e:
            print(f"Error occurred when select_product_sku_by_asin: {e}")
    def select_sp_sspu_name(self,sspu):
        try:
            conn = self.conn
            sspu1 = sspu.lower()
            query = """
SELECT DISTINCT campaign_name,campaignId FROM amazon_campaigns_list_sp
WHERE market = '{}'
AND state != 'ARCHIVED'
AND (campaign_name LIKE '%{}%' OR campaign_name LIKE '%{}%')
                    """.format(self.market,sspu,sspu1)
            df = pd.read_sql(query, con=conn)
            if df.empty:
                print("No campaignName")
                return None, None
            else:
                print("select campaignName success")
                return df['campaign_name'].tolist(), df['campaignId'].tolist()
        except Exception as e:
            print(f"Error occurred when select_product_sku_by_asin: {e}")

    def select_sd_sspu_name(self,sspu):
        try:
            conn = self.conn
            sspu1 = sspu.lower()
            query = """
SELECT DISTINCT campaignName,campaignId FROM amazon_campaigns_list_sd
WHERE market = '{}'
AND state != 'archived'
AND (campaignName LIKE '%{}%' OR campaignName LIKE '%{}%')
                    """.format(self.market,sspu,sspu1)
            df = pd.read_sql(query, con=conn)
            if df.empty:
                print("No campaignName")
                return None, None
            else:
                print("select campaignName success")
                return df['campaignName'].tolist(), df['campaignId'].tolist()
        except Exception as e:
            print(f"Error occurred when select_sd_sspu_name: {e}")

    def select_sp_sspu_name_overstock(self,sspu):
        try:
            conn = self.conn
            sspu1 = sspu.lower()
            query = """
SELECT DISTINCT campaign_name, campaignId
FROM amazon_campaigns_list_sp
WHERE
    market = '{}' AND
    campaign_name LIKE '%_overstock' AND
    (
        campaign_name LIKE '%{}%' OR
        campaign_name LIKE '%{}%'
    )
                    """.format(self.market,sspu,sspu1)
            df = pd.read_sql(query, con=conn)
            if df.empty:
                print("No campaignName")
                return None, None
            else:
                print("select campaignName success")
                return df['campaign_name'].tolist(), df['campaignId'].tolist()
        except Exception as e:
            print(f"Error occurred when select_product_sku_by_asin: {e}")

    def select_sd_sspu_name_overstock(self,sspu):
        try:
            conn = self.conn
            sspu1 = sspu.lower()
            query = """
SELECT DISTINCT campaignName, campaignId
FROM amazon_campaigns_list_sd
WHERE
    market = '{}' AND
    campaignName LIKE '%_overstock' AND
    (
        campaignName LIKE '%{}%' OR
        campaignName LIKE '%{}%'
    )
                    """.format(self.market,sspu,sspu1)
            df = pd.read_sql(query, con=conn)
            if df.empty:
                print("No campaignName")
                return None, None
            else:
                print("select campaignName success")
                return df['campaignName'].tolist(), df['campaignId'].tolist()
        except Exception as e:
            print(f"Error occurred when select_sd_sspu_name: {e}")

    def select_sp_campaign(self):
        try:
            conn = self.conn
            query = """
SELECT DISTINCT campaignId FROM amazon_campaigns_list_sp
WHERE market = '{}'
AND state = 'ENABLED'
                    """.format(self.market)
            df = pd.read_sql(query, con=conn)
            if df.empty:
                print("No campaignId")
                return None
            else:
                print("select campaignId success")
                return df['campaignId'].tolist()
        except Exception as e:
            print(f"Error occurred when select_product_sku_by_asin: {e}")

    def select_sp_campaignid_search_term(self,curtime,campaignid):
        try:
            conn = self.conn
            query = """
WITH Campaign_Stats AS (
    SELECT
        acr.campaignId,
        acr.campaignName,
        acr.campaignBudgetAmount AS Budget,
        acr.market,
        SUM(CASE WHEN acr.date = DATE_SUB('{}', INTERVAL 2 DAY) THEN acr.cost ELSE 0 END) AS cost_yesterday,
        SUM(CASE WHEN acr.date = DATE_SUB('{}', INTERVAL 2 DAY) THEN acr.clicks ELSE 0 END) AS clicks_yesterday,
        SUM(CASE WHEN acr.date = DATE_SUB('{}', INTERVAL 2 DAY) THEN acr.sales14d ELSE 0 END) AS sales_yesterday,
        SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{}' - INTERVAL 1 DAY, INTERVAL 6 DAY) AND DATE_SUB('{}', INTERVAL 1 DAY) THEN acr.cost ELSE 0 END) AS total_cost_7d,
        SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{}' - INTERVAL 1 DAY, INTERVAL 6 DAY) AND DATE_SUB('{}', INTERVAL 1 DAY) THEN acr.sales14d ELSE 0 END) AS total_sales14d_7d,
        SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{}' - INTERVAL 1 DAY, INTERVAL 29 DAY) AND DATE_SUB('{}', INTERVAL 1 DAY) THEN acr.cost ELSE 0 END) AS total_cost_30d,
        SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{}' - INTERVAL 1 DAY, INTERVAL 29 DAY) AND DATE_SUB('{}', INTERVAL 1 DAY) THEN acr.sales14d ELSE 0 END) AS total_sales14d_30d,
        SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{}' - INTERVAL 1 DAY, INTERVAL 29 DAY) AND DATE_SUB('{}', INTERVAL 1 DAY) THEN acr.clicks ELSE 0 END) AS total_clicks_30d,
        SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{}' - INTERVAL 1 DAY, INTERVAL 6 DAY) AND DATE_SUB('{}', INTERVAL 1 DAY) THEN acr.clicks ELSE 0 END) AS total_clicks_7d,
        SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{}' - INTERVAL 1 DAY, INTERVAL 29 DAY) AND DATE_SUB('{}', INTERVAL 1 DAY) THEN acr.cost ELSE 0 END) / NULLIF(SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{}' - INTERVAL 1 DAY, INTERVAL 29 DAY) AND DATE_SUB('{}', INTERVAL 1 DAY) THEN acr.sales14d ELSE 0 END), 0) AS ACOS_30d,
        SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{}' - INTERVAL 1 DAY, INTERVAL 6 DAY) AND DATE_SUB('{}', INTERVAL 1 DAY) THEN acr.cost ELSE 0 END) / NULLIF(SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{}' - INTERVAL 1 DAY, INTERVAL 6 DAY) AND DATE_SUB('{}', INTERVAL 1 DAY) THEN acr.sales14d ELSE 0 END), 0) AS ACOS_7d,
        SUM(CASE WHEN acr.date = '{}' - INTERVAL 2 DAY THEN acr.cost ELSE 0 END) / NULLIF(SUM(CASE WHEN acr.date = '{}' - INTERVAL 2 DAY THEN acr.sales14d ELSE 0 END), 0)  AS ACOS_yesterday
    FROM
        amazon_campaign_reports_sp acr
    JOIN amazon_campaigns_list_sp acl ON acr.campaignId = acl.campaignId
    WHERE
        acr.date BETWEEN DATE_SUB('{}', INTERVAL 30 DAY)
        AND ('{}' - INTERVAL 1 DAY)
        AND acr.campaignId IN (SELECT campaignId FROM amazon_campaign_reports_sp WHERE campaignStatus = 'ENABLED' AND date = '{}' - INTERVAL 1 DAY )
        AND acr.market = '{}'
    GROUP BY
        acr.campaignName
),
b AS (
    SELECT
        SUM(reports.cost) / SUM(reports.sales14d) AS country_avg_ACOS_1m,
        reports.market
    FROM
        amazon_campaign_reports_sp AS reports
    INNER JOIN amazon_campaigns_list_sp AS campaigns ON reports.campaignId = campaigns.campaignId
    WHERE
        reports.date BETWEEN DATE_SUB('{}', INTERVAL 30 DAY)
        AND ('{}' - INTERVAL 1 DAY)
        AND campaigns.campaignId IN (SELECT campaignId FROM amazon_campaign_reports_sp WHERE campaignStatus = 'ENABLED' AND date = '{}' - INTERVAL 1 DAY)
        AND reports.market = '{}'
    GROUP BY
        reports.market
),
TargetCampaignIds AS (
    SELECT DISTINCT campaignId, adGroupId
    FROM amazon_sp_productads_list AS T1
    WHERE EXISTS (
        SELECT 1
        FROM amazon_sp_productads_list AS T2
        WHERE T2.campaignId = {}
          AND T2.market = '{}'
          AND T2.asin = T1.asin
      )
      AND EXISTS (
        SELECT 1
        FROM amazon_keywords_list_sp AS T4
        WHERE T4.campaignId = T1.campaignId
          AND T4.market = '{}'
          AND T4.keywordText != '(_targeting_auto_)'
          AND T4.extendedData_servingStatus ='TARGETING_CLAUSE_STATUS_LIVE'
      )
    GROUP BY T1.campaignId, T1.adGroupId
    HAVING COUNT(DISTINCT CASE WHEN T1.campaignId = {} THEN T1.asin ELSE NULL END) * 1.0 / COUNT(DISTINCT T1.asin) <= 0.5
),
CampaignStatsResult AS (
  SELECT
    tci.adGroupId,
    cs.*,
    b.country_avg_ACOS_1m
FROM
    Campaign_Stats cs
JOIN b ON cs.market = b.market
JOIN TargetCampaignIds tci ON cs.campaignId = tci.campaignId
WHERE
  cs.campaignId IN (SELECT campaignId FROM TargetCampaignIds)
  AND (SELECT COUNT(DISTINCT campaignId) FROM TargetCampaignIds) = 1
UNION ALL
SELECT
    tci.adGroupId,
    cs.*,
    b.country_avg_ACOS_1m
FROM
    Campaign_Stats cs
JOIN b ON cs.market = b.market
JOIN TargetCampaignIds tci ON cs.campaignId = tci.campaignId
WHERE (SELECT COUNT(DISTINCT campaignId) FROM TargetCampaignIds) > 1 AND (cs.ACOS_30d <= 0.36 OR cs.ACOS_30d IS NULL)
)
SELECT
    *
FROM
    CampaignStatsResult
ORDER BY
    total_sales14d_30d DESC
LIMIT 1
                    """.format(curtime,curtime,curtime,curtime,curtime,curtime,curtime,curtime,curtime,curtime,
                               curtime,curtime,curtime,curtime,curtime,curtime,curtime,curtime,curtime,curtime,
                               curtime,curtime,curtime,curtime,curtime,curtime,curtime,curtime,self.market,curtime,curtime,curtime,self.market,campaignid,self.market,self.market,campaignid)
            df = pd.read_sql(query, con=conn)
            if df.empty:
                print("No campaignId")
                return None,None,None
            else:
                print("select campaignId success")
                return df.loc[0,'campaignId'],df.loc[0,'campaignName'],df.loc[0,'adGroupId']
        except Exception as e:
            print(f"Error occurred when select_product_sku_by_asin: {e}")

    def select_sp_campaignid_search_term_jiutong(self, curtime, campaignid):
        try:
            conn = self.conn
            query = """
WITH Campaign_Stats AS (
    SELECT
        acr.campaignId,
        acr.campaignName,
        acr.campaignBudgetAmount AS Budget,
        acr.market,
        SUM(CASE WHEN acr.date = DATE_SUB('{}', INTERVAL 2 DAY) THEN acr.cost ELSE 0 END) AS cost_yesterday,
        SUM(CASE WHEN acr.date = DATE_SUB('{}', INTERVAL 2 DAY) THEN acr.clicks ELSE 0 END) AS clicks_yesterday,
        SUM(CASE WHEN acr.date = DATE_SUB('{}', INTERVAL 2 DAY) THEN acr.sales14d ELSE 0 END) AS sales_yesterday,
        SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{}' - INTERVAL 1 DAY, INTERVAL 6 DAY) AND DATE_SUB('{}', INTERVAL 1 DAY) THEN acr.cost ELSE 0 END) AS total_cost_7d,
        SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{}' - INTERVAL 1 DAY, INTERVAL 6 DAY) AND DATE_SUB('{}', INTERVAL 1 DAY) THEN acr.sales14d ELSE 0 END) AS total_sales14d_7d,
        SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{}' - INTERVAL 1 DAY, INTERVAL 29 DAY) AND DATE_SUB('{}', INTERVAL 1 DAY) THEN acr.cost ELSE 0 END) AS total_cost_30d,
        SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{}' - INTERVAL 1 DAY, INTERVAL 29 DAY) AND DATE_SUB('{}', INTERVAL 1 DAY) THEN acr.sales14d ELSE 0 END) AS total_sales14d_30d,
        SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{}' - INTERVAL 1 DAY, INTERVAL 29 DAY) AND DATE_SUB('{}', INTERVAL 1 DAY) THEN acr.clicks ELSE 0 END) AS total_clicks_30d,
        SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{}' - INTERVAL 1 DAY, INTERVAL 6 DAY) AND DATE_SUB('{}', INTERVAL 1 DAY) THEN acr.clicks ELSE 0 END) AS total_clicks_7d,
        SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{}' - INTERVAL 1 DAY, INTERVAL 29 DAY) AND DATE_SUB('{}', INTERVAL 1 DAY) THEN acr.cost ELSE 0 END) / NULLIF(SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{}' - INTERVAL 1 DAY, INTERVAL 29 DAY) AND DATE_SUB('{}', INTERVAL 1 DAY) THEN acr.sales14d ELSE 0 END), 0) AS ACOS_30d,
        SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{}' - INTERVAL 1 DAY, INTERVAL 6 DAY) AND DATE_SUB('{}', INTERVAL 1 DAY) THEN acr.cost ELSE 0 END) / NULLIF(SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{}' - INTERVAL 1 DAY, INTERVAL 6 DAY) AND DATE_SUB('{}', INTERVAL 1 DAY) THEN acr.sales14d ELSE 0 END), 0) AS ACOS_7d,
        SUM(CASE WHEN acr.date = '{}' - INTERVAL 2 DAY THEN acr.cost ELSE 0 END) / NULLIF(SUM(CASE WHEN acr.date = '{}' - INTERVAL 2 DAY THEN acr.sales14d ELSE 0 END), 0)  AS ACOS_yesterday
    FROM
        amazon_campaign_reports_sp acr
    JOIN amazon_campaigns_list_sp acl ON acr.campaignId = acl.campaignId
    WHERE
        acr.date BETWEEN DATE_SUB('{}', INTERVAL 30 DAY)
        AND ('{}' - INTERVAL 1 DAY)
        AND acr.campaignId IN (SELECT campaignId FROM amazon_campaign_reports_sp WHERE campaignStatus = 'ENABLED' AND date = '{}' - INTERVAL 1 DAY )
        AND acr.market = '{}'
    GROUP BY
        acr.campaignName
),
b AS (
    SELECT
        SUM(reports.cost) / SUM(reports.sales14d) AS country_avg_ACOS_1m,
        reports.market
    FROM
        amazon_campaign_reports_sp AS reports
    INNER JOIN amazon_campaigns_list_sp AS campaigns ON reports.campaignId = campaigns.campaignId
    WHERE
        reports.date BETWEEN DATE_SUB('{}', INTERVAL 30 DAY)
        AND ('{}' - INTERVAL 1 DAY)
        AND campaigns.campaignId IN (SELECT campaignId FROM amazon_campaign_reports_sp WHERE campaignStatus = 'ENABLED' AND date = '{}' - INTERVAL 1 DAY)
        AND reports.market = '{}'
    GROUP BY
        reports.market
),
TargetCampaignIds AS (
    SELECT DISTINCT campaignId, adGroupId
    FROM amazon_sp_productads_list AS T1
    WHERE EXISTS (
        SELECT 1
        FROM amazon_sp_productads_list AS T2
        WHERE T2.campaignId = {}
          AND T2.market = '{}'
          AND T2.asin = T1.asin
      )
      AND EXISTS (
        SELECT 1
        FROM amazon_keywords_list_sp AS T4
        WHERE T4.campaignId = T1.campaignId
          AND T4.market = '{}'
          AND T4.keywordText != '(_targeting_auto_)'
          AND T4.extendedData_servingStatus ='TARGETING_CLAUSE_STATUS_LIVE'
      )
    GROUP BY T1.campaignId, T1.adGroupId
    HAVING COUNT(DISTINCT CASE WHEN T1.campaignId = {} THEN T1.asin ELSE NULL END) * 1.0 / COUNT(DISTINCT T1.asin) <= 0.5
),
CampaignStatsResult AS (
  SELECT
    tci.adGroupId, --  从TargetCampaignIds中选择adGroupId, 放置在campaignId之前
    cs.*,
    b.country_avg_ACOS_1m
  FROM
    Campaign_Stats cs
  JOIN b ON cs.market = b.market
  JOIN TargetCampaignIds tci ON cs.campaignId = tci.campaignId
  WHERE
    cs.campaignId IN (SELECT campaignId FROM TargetCampaignIds)
    AND cs.campaignName LIKE '%Deep%'
)
SELECT
    *
FROM
    CampaignStatsResult
ORDER BY
    total_sales14d_30d DESC
LIMIT 1
                    """.format(curtime, curtime, curtime, curtime, curtime, curtime, curtime, curtime, curtime,
                               curtime,
                               curtime, curtime, curtime, curtime, curtime, curtime, curtime, curtime, curtime,
                               curtime,
                               curtime, curtime, curtime, curtime, curtime, curtime, curtime, curtime, self.market,
                               curtime, curtime, curtime, self.market, campaignid, self.market, self.market, campaignid)
            df = pd.read_sql(query, con=conn)
            if df.empty:
                print("No campaignId")
                return None, None, None
            else:
                print("select campaignId success")
                return df.loc[0, 'campaignId'], df.loc[0, 'campaignName'], df.loc[0, 'adGroupId']
        except Exception as e:
            print(f"Error occurred when select_product_sku_by_asin: {e}")

    def select_sp_asin_campaignid_search_term(self, curtime, campaignid):
        try:
            conn = self.conn
            query = f"""
WITH Campaign_Stats AS (
    SELECT
        acr.campaignId,
        acr.campaignName,
        acr.campaignBudgetAmount AS Budget,
        acr.market,
        SUM(CASE WHEN acr.date = DATE_SUB('{curtime}', INTERVAL 2 DAY) THEN acr.cost ELSE 0 END) AS cost_yesterday,
        SUM(CASE WHEN acr.date = DATE_SUB('{curtime}', INTERVAL 2 DAY) THEN acr.clicks ELSE 0 END) AS clicks_yesterday,
        SUM(CASE WHEN acr.date = DATE_SUB('{curtime}', INTERVAL 2 DAY) THEN acr.sales14d ELSE 0 END) AS sales_yesterday,
        SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{curtime}' - INTERVAL 1 DAY, INTERVAL 6 DAY) AND DATE_SUB('{curtime}', INTERVAL 1 DAY) THEN acr.cost ELSE 0 END) AS total_cost_7d,
        SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{curtime}' - INTERVAL 1 DAY, INTERVAL 6 DAY) AND DATE_SUB('{curtime}', INTERVAL 1 DAY) THEN acr.sales14d ELSE 0 END) AS total_sales14d_7d,
        SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{curtime}' - INTERVAL 1 DAY, INTERVAL 29 DAY) AND DATE_SUB('{curtime}', INTERVAL 1 DAY) THEN acr.cost ELSE 0 END) AS total_cost_30d,
        SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{curtime}' - INTERVAL 1 DAY, INTERVAL 29 DAY) AND DATE_SUB('{curtime}', INTERVAL 1 DAY) THEN acr.sales14d ELSE 0 END) AS total_sales14d_30d,
        SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{curtime}' - INTERVAL 1 DAY, INTERVAL 29 DAY) AND DATE_SUB('{curtime}', INTERVAL 1 DAY) THEN acr.clicks ELSE 0 END) AS total_clicks_30d,
        SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{curtime}' - INTERVAL 1 DAY, INTERVAL 6 DAY) AND DATE_SUB('{curtime}', INTERVAL 1 DAY) THEN acr.clicks ELSE 0 END) AS total_clicks_7d,
        SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{curtime}' - INTERVAL 1 DAY, INTERVAL 29 DAY) AND DATE_SUB('{curtime}', INTERVAL 1 DAY) THEN acr.cost ELSE 0 END) / NULLIF(SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{curtime}' - INTERVAL 1 DAY, INTERVAL 29 DAY) AND DATE_SUB('{curtime}', INTERVAL 1 DAY) THEN acr.sales14d ELSE 0 END), 0) AS ACOS_30d,
        SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{curtime}' - INTERVAL 1 DAY, INTERVAL 6 DAY) AND DATE_SUB('{curtime}', INTERVAL 1 DAY) THEN acr.cost ELSE 0 END) / NULLIF(SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{curtime}' - INTERVAL 1 DAY, INTERVAL 6 DAY) AND DATE_SUB('{curtime}', INTERVAL 1 DAY) THEN acr.sales14d ELSE 0 END), 0) AS ACOS_7d,
        SUM(CASE WHEN acr.date = '{curtime}' - INTERVAL 2 DAY THEN acr.cost ELSE 0 END) / NULLIF(SUM(CASE WHEN acr.date = '{curtime}' - INTERVAL 2 DAY THEN acr.sales14d ELSE 0 END), 0)  AS ACOS_yesterday
    FROM
        amazon_campaign_reports_sp acr
    JOIN amazon_campaigns_list_sp acl ON acr.campaignId = acl.campaignId
    WHERE
        acr.date BETWEEN DATE_SUB('{curtime}', INTERVAL 30 DAY)
        AND ('{curtime}' - INTERVAL 1 DAY)
        AND acr.campaignId IN (SELECT campaignId FROM amazon_campaign_reports_sp WHERE campaignStatus = 'ENABLED' AND date = '{curtime}' - INTERVAL 1 DAY )
        AND acr.market = '{self.market}'
    GROUP BY
        acr.campaignName
),
b AS (
    SELECT
        SUM(reports.cost) / SUM(reports.sales14d) AS country_avg_ACOS_1m,
        reports.market
    FROM
        amazon_campaign_reports_sp AS reports
    INNER JOIN amazon_campaigns_list_sp AS campaigns ON reports.campaignId = campaigns.campaignId
    WHERE
        reports.date BETWEEN DATE_SUB('{curtime}', INTERVAL 30 DAY)
        AND ('{curtime}' - INTERVAL 1 DAY)
        AND campaigns.campaignId IN (SELECT campaignId FROM amazon_campaign_reports_sp WHERE campaignStatus = 'ENABLED' AND date = '{curtime}' - INTERVAL 1 DAY)
        AND reports.market = '{self.market}'
    GROUP BY
        reports.market
),
TargetCampaignIds AS (
SELECT DISTINCT T1.adGroupId, T3.campaignId, T3.targetingType, T3.campaign_name, T3.state AS campaignStatus
FROM amazon_sp_productads_list AS T1
INNER JOIN amazon_campaigns_list_sp AS T3 ON T1.campaignId = T3.campaignId AND T3.market = '{self.market}'
WHERE T3.targetingType = 'MANUAL' AND T3.state = 'ENABLED'
  AND EXISTS (
    SELECT 1
    FROM amazon_sp_productads_list AS T2
    WHERE T2.campaignId = '{campaignid}'
      AND T2.market = '{self.market}'
      AND T2.asin = T1.asin
  )
  AND (T3.campaign_name LIKE '%0514%' OR T3.campaign_name LIKE '%ASIN%')
GROUP BY T1.adGroupId,T3.campaign_name, T3.state
HAVING COUNT(DISTINCT CASE WHEN T1.campaignId = '{campaignid}' THEN T1.asin ELSE NULL END) * 1.0 / COUNT(DISTINCT T1.asin) <= 0.5
),
CampaignStatsResult AS (
  SELECT
    cs.*,
    b.country_avg_ACOS_1m
FROM
    Campaign_Stats cs
JOIN b ON cs.market = b.market
WHERE
  cs.campaignId IN (SELECT campaignId FROM TargetCampaignIds)
  AND (SELECT COUNT(DISTINCT campaignId) FROM TargetCampaignIds) = 1
UNION ALL
SELECT
    cs.*,
    b.country_avg_ACOS_1m
FROM
    Campaign_Stats cs
JOIN b ON cs.market = b.market
JOIN TargetCampaignIds tci ON cs.campaignId = tci.campaignId
WHERE (SELECT COUNT(DISTINCT campaignId) FROM TargetCampaignIds) > 1 AND (cs.ACOS_30d <= 0.36 OR cs.ACOS_30d IS NULL)
)
SELECT
    tci.adGroupId,
    cs.*
FROM
    CampaignStatsResult cs
LEFT JOIN TargetCampaignIds tci ON cs.campaignId = tci.campaignId
ORDER BY
    total_sales14d_30d DESC
LIMIT 1;
                    """
            df = pd.read_sql(query, con=conn)
            if df.empty:
                print("No campaignId")
                return None, None, None
            else:
                print("select campaignId success")
                return df.loc[0, 'campaignId'], df.loc[0, 'campaignName'], df.loc[0, 'adGroupId']
        except Exception as e:
            print(f"Error occurred when select_product_sku_by_asin: {e}")

    def select_sp_asin_campaignid_search_term_jiutong(self, curtime, campaignid):
        try:
            conn = self.conn
            query = f"""
WITH Campaign_Stats AS (
    SELECT
        acr.campaignId,
        acr.campaignName,
        acr.campaignBudgetAmount AS Budget,
        acr.market,
        SUM(CASE WHEN acr.date = DATE_SUB('{curtime}', INTERVAL 2 DAY) THEN acr.cost ELSE 0 END) AS cost_yesterday,
        SUM(CASE WHEN acr.date = DATE_SUB('{curtime}', INTERVAL 2 DAY) THEN acr.clicks ELSE 0 END) AS clicks_yesterday,
        SUM(CASE WHEN acr.date = DATE_SUB('{curtime}', INTERVAL 2 DAY) THEN acr.sales14d ELSE 0 END) AS sales_yesterday,
        SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{curtime}' - INTERVAL 1 DAY, INTERVAL 6 DAY) AND DATE_SUB('{curtime}', INTERVAL 1 DAY) THEN acr.cost ELSE 0 END) AS total_cost_7d,
        SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{curtime}' - INTERVAL 1 DAY, INTERVAL 6 DAY) AND DATE_SUB('{curtime}', INTERVAL 1 DAY) THEN acr.sales14d ELSE 0 END) AS total_sales14d_7d,
        SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{curtime}' - INTERVAL 1 DAY, INTERVAL 29 DAY) AND DATE_SUB('{curtime}', INTERVAL 1 DAY) THEN acr.cost ELSE 0 END) AS total_cost_30d,
        SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{curtime}' - INTERVAL 1 DAY, INTERVAL 29 DAY) AND DATE_SUB('{curtime}', INTERVAL 1 DAY) THEN acr.sales14d ELSE 0 END) AS total_sales14d_30d,
        SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{curtime}' - INTERVAL 1 DAY, INTERVAL 29 DAY) AND DATE_SUB('{curtime}', INTERVAL 1 DAY) THEN acr.clicks ELSE 0 END) AS total_clicks_30d,
        SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{curtime}' - INTERVAL 1 DAY, INTERVAL 6 DAY) AND DATE_SUB('{curtime}', INTERVAL 1 DAY) THEN acr.clicks ELSE 0 END) AS total_clicks_7d,
        SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{curtime}' - INTERVAL 1 DAY, INTERVAL 29 DAY) AND DATE_SUB('{curtime}', INTERVAL 1 DAY) THEN acr.cost ELSE 0 END) / NULLIF(SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{curtime}' - INTERVAL 1 DAY, INTERVAL 29 DAY) AND DATE_SUB('{curtime}', INTERVAL 1 DAY) THEN acr.sales14d ELSE 0 END), 0) AS ACOS_30d,
        SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{curtime}' - INTERVAL 1 DAY, INTERVAL 6 DAY) AND DATE_SUB('{curtime}', INTERVAL 1 DAY) THEN acr.cost ELSE 0 END) / NULLIF(SUM(CASE WHEN acr.date BETWEEN DATE_SUB('{curtime}' - INTERVAL 1 DAY, INTERVAL 6 DAY) AND DATE_SUB('{curtime}', INTERVAL 1 DAY) THEN acr.sales14d ELSE 0 END), 0) AS ACOS_7d,
        SUM(CASE WHEN acr.date = '{curtime}' - INTERVAL 2 DAY THEN acr.cost ELSE 0 END) / NULLIF(SUM(CASE WHEN acr.date = '{curtime}' - INTERVAL 2 DAY THEN acr.sales14d ELSE 0 END), 0)  AS ACOS_yesterday
    FROM
        amazon_campaign_reports_sp acr
    JOIN amazon_campaigns_list_sp acl ON acr.campaignId = acl.campaignId
    WHERE
        acr.date BETWEEN DATE_SUB('{curtime}', INTERVAL 30 DAY)
        AND ('{curtime}' - INTERVAL 1 DAY)
        AND acr.campaignId IN (SELECT campaignId FROM amazon_campaign_reports_sp WHERE campaignStatus = 'ENABLED' AND date = '{curtime}' - INTERVAL 1 DAY )
        AND acr.market = '{self.market}'
    GROUP BY
        acr.campaignName
),
b AS (
    SELECT
        SUM(reports.cost) / SUM(reports.sales14d) AS country_avg_ACOS_1m,
        reports.market
    FROM
        amazon_campaign_reports_sp AS reports
    INNER JOIN amazon_campaigns_list_sp AS campaigns ON reports.campaignId = campaigns.campaignId
    WHERE
        reports.date BETWEEN DATE_SUB('{curtime}', INTERVAL 30 DAY)
        AND ('{curtime}' - INTERVAL 1 DAY)
        AND campaigns.campaignId IN (SELECT campaignId FROM amazon_campaign_reports_sp WHERE campaignStatus = 'ENABLED' AND date = '{curtime}' - INTERVAL 1 DAY)
        AND reports.market = '{self.market}'
    GROUP BY
        reports.market
),
TargetCampaignIds AS (
SELECT DISTINCT T1.adGroupId, T3.campaignId, T3.targetingType, T3.campaign_name, T3.state AS campaignStatus
FROM amazon_sp_productads_list AS T1
INNER JOIN amazon_campaigns_list_sp AS T3 ON T1.campaignId = T3.campaignId AND T3.market = '{self.market}'
WHERE T3.targetingType = 'MANUAL' AND T3.state = 'ENABLED'
  AND EXISTS (
    SELECT 1
    FROM amazon_sp_productads_list AS T2
    WHERE T2.campaignId = '{campaignid}'
      AND T2.market = '{self.market}'
      AND T2.asin = T1.asin
  )
  AND (T3.campaign_name LIKE '%0514%')
GROUP BY T1.adGroupId,T3.campaign_name, T3.state
HAVING COUNT(DISTINCT CASE WHEN T1.campaignId = '{campaignid}' THEN T1.asin ELSE NULL END) * 1.0 / COUNT(DISTINCT T1.asin) <= 0.5
),
CampaignStatsResult AS (
  SELECT
    cs.*,
    b.country_avg_ACOS_1m
FROM
    Campaign_Stats cs
JOIN b ON cs.market = b.market
WHERE
  cs.campaignId IN (SELECT campaignId FROM TargetCampaignIds)
  AND (SELECT COUNT(DISTINCT campaignId) FROM TargetCampaignIds) = 1
UNION ALL
SELECT
    cs.*,
    b.country_avg_ACOS_1m
FROM
    Campaign_Stats cs
JOIN b ON cs.market = b.market
JOIN TargetCampaignIds tci ON cs.campaignId = tci.campaignId
WHERE (SELECT COUNT(DISTINCT campaignId) FROM TargetCampaignIds) > 1 AND (cs.ACOS_30d <= 0.36 OR cs.ACOS_30d IS NULL)
)
SELECT
    tci.adGroupId,
    cs.*
FROM
    CampaignStatsResult cs
LEFT JOIN TargetCampaignIds tci ON cs.campaignId = tci.campaignId
ORDER BY
    total_sales14d_30d DESC
LIMIT 1;
                    """
            df = pd.read_sql(query, con=conn)
            if df.empty:
                print("No campaignId")
                return None, None, None
            else:
                print("select campaignId success")
                return df.loc[0, 'campaignId'], df.loc[0, 'campaignName'], df.loc[0, 'adGroupId']
        except Exception as e:
            print(f"Error occurred when select_product_sku_by_asin: {e}")

    def select_sp_campaign_search_term(self,sspu):
        try:
            conn = self.conn
            query = f"""
SELECT
    b.sspu,
    a.searchTerm,
    a.keyword,
    a.keywordBid,
    a.adGroupName,
    a.adGroupId,
    a.matchType,
    a.campaignName,
    a.campaignId,
    SUM(CASE WHEN a.date BETWEEN DATE_SUB(CURDATE()- INTERVAL 1 DAY - INTERVAL 1 DAY, INTERVAL 29 day) AND DATE_SUB(CURDATE()- INTERVAL 1 DAY, INTERVAL 1 DAY) THEN a.clicks ELSE 0 END) AS total_clicks_30d,
    SUM(CASE WHEN a.date BETWEEN DATE_SUB(CURDATE()- INTERVAL 1 DAY - INTERVAL 1 DAY, INTERVAL 6 DAY) AND DATE_SUB(CURDATE()- INTERVAL 1 DAY, INTERVAL 1 DAY) THEN a.clicks ELSE 0 END) AS total_clicks_7d,
    SUM(CASE WHEN a.date = CURDATE()- INTERVAL 1 DAY - INTERVAL 2 DAY THEN a.clicks ELSE 0 END) AS total_clicks_yesterday,
    SUM(CASE WHEN a.date BETWEEN DATE_SUB(CURDATE()- INTERVAL 1 DAY - INTERVAL 1 DAY, INTERVAL 29 day) AND DATE_SUB(CURDATE()- INTERVAL 1 DAY, INTERVAL 1 DAY) THEN a.sales14d ELSE 0 END) AS total_sales14d_30d,
    SUM(CASE WHEN a.date BETWEEN DATE_SUB(CURDATE()- INTERVAL 1 DAY - INTERVAL 1 DAY, INTERVAL 6 DAY) AND DATE_SUB(CURDATE()- INTERVAL 1 DAY, INTERVAL 1 DAY) THEN a.sales14d ELSE 0 END) AS total_sales14d_7d,
    SUM(CASE WHEN a.date = CURDATE()- INTERVAL 1 DAY - INTERVAL 2 DAY THEN a.sales14d ELSE 0 END) AS total_sales14d_yesterday,
    SUM(CASE WHEN a.date BETWEEN DATE_SUB(CURDATE()- INTERVAL 1 DAY - INTERVAL 1 DAY, INTERVAL 29 day) AND DATE_SUB(CURDATE()- INTERVAL 1 DAY, INTERVAL 1 DAY) THEN a.cost ELSE 0 END) AS total_cost_30d,
    SUM(CASE WHEN a.date BETWEEN DATE_SUB(CURDATE()- INTERVAL 1 DAY - INTERVAL 1 DAY, INTERVAL 6 DAY) AND DATE_SUB(CURDATE()- INTERVAL 1 DAY, INTERVAL 1 DAY) THEN a.cost ELSE 0 END) AS total_cost_7d,
    SUM(CASE WHEN a.date = CURDATE()- INTERVAL 1 DAY - INTERVAL 2 DAY THEN a.cost ELSE 0 END) AS total_cost_yesterday,
    SUM(CASE WHEN a.date BETWEEN DATE_SUB(CURDATE()- INTERVAL 1 DAY - INTERVAL 1 DAY, INTERVAL 29 day) AND DATE_SUB(CURDATE()- INTERVAL 1 DAY, INTERVAL 1 DAY) THEN a.cost ELSE 0 END) / SUM(CASE WHEN a.date BETWEEN DATE_SUB(CURDATE()- INTERVAL 1 DAY - INTERVAL 1 DAY, INTERVAL 29 day) AND DATE_SUB(CURDATE()- INTERVAL 1 DAY, INTERVAL 1 DAY) THEN a.sales14d ELSE 0 END) AS ACOS_30d,
    SUM(CASE WHEN a.date BETWEEN DATE_SUB(CURDATE()- INTERVAL 1 DAY - INTERVAL 1 DAY, INTERVAL 6 DAY) AND DATE_SUB(CURDATE()- INTERVAL 1 DAY, INTERVAL 1 DAY) THEN a.cost ELSE 0 END) / SUM(CASE WHEN a.date BETWEEN DATE_SUB(CURDATE()- INTERVAL 1 DAY - INTERVAL 1 DAY, INTERVAL 6 DAY) AND DATE_SUB(CURDATE()- INTERVAL 1 DAY, INTERVAL 1 DAY) THEN a.sales14d ELSE 0 END) AS ACOS_7d,
    SUM(CASE WHEN a.date = CURDATE()- INTERVAL 1 DAY - INTERVAL 2 DAY THEN a.cost ELSE 0 END) / SUM(CASE WHEN a.date = CURDATE()- INTERVAL 1 DAY - INTERVAL 2 DAY THEN a.sales14d ELSE 0 END)  AS ACOS_yesterday,
    SUM(CASE WHEN a.date BETWEEN DATE_SUB(CURDATE()- INTERVAL 1 DAY - INTERVAL 1 DAY, INTERVAL 29 day) AND DATE_SUB(CURDATE()- INTERVAL 1 DAY, INTERVAL 1 DAY) THEN a.purchases7d ELSE 0 END) AS ORDER_1m,
    SUM(CASE WHEN a.date BETWEEN DATE_SUB(CURDATE()- INTERVAL 1 DAY - INTERVAL 1 DAY, INTERVAL 6 day) AND DATE_SUB(CURDATE()- INTERVAL 1 DAY, INTERVAL 1 DAY) THEN a.purchases7d ELSE 0 END) AS ORDER_7d

FROM
    amazon_search_term_reports_sp a
JOIN
    amazon_campaigns_list_sp c ON a.campaignId = c.campaignId
JOIN
    (select sspu,campaignId
    from amazon_advertised_product_reports_sp t1
    join
        prod_as_product_base t2 ON t2.sku = t1.advertisedSku
    where market = '{self.market}'
    group by
        campaignId
    ) b ON c.campaignId = b.campaignId
WHERE
    a.date BETWEEN DATE_SUB(CURDATE()- INTERVAL 1 DAY, INTERVAL 30 DAY) AND CURDATE()- INTERVAL 1 DAY- INTERVAL 1 DAY
    AND a.market = '{self.market}'
    AND b.sspu = '{sspu}'
    AND c.state = 'ENABLED'
    AND c.targetingType LIKE '%AUT%'
    AND NOT (a.searchTerm LIKE 'b0%' AND LENGTH(a.searchTerm) = 10) -- 添加排除条件
GROUP BY
    a.adGroupName,
    a.campaignName,
    a.keyword,
    a.searchTerm,
    a.matchType
ORDER BY
    a.adGroupName,
    a.campaignName,
    a.keyword,
    a.searchTerm;
                    """.format(self.market)
            df = pd.read_sql(query, con=conn)
            if df.empty:
                print("No search_term")
                return None
            else:
                # Define criteria for filtering
                # Criteria 1: Sales in the last 7 days > 0 and ACOS in the last 7 days <= 0.24
                criteria1 = (df['total_sales14d_7d'] > 0) & (df['ACOS_7d'] <= 0.24)

                # Criteria 2: Orders in the last 30 days >= 2 and average ACOS in the last 30 days <= 0.24
                criteria2 = (df['ORDER_1m'] >= 2) & (df['ACOS_30d'] <= 0.24)

                # Apply filters
                filtered_df = df[criteria1 | criteria2]

                if filtered_df.empty:
                    print("No search_term matching the criteria")
                    return None
                else:
                    print("select campaignId success")
                    return filtered_df['searchTerm'].tolist()

        except Exception as e:
            print(f"Error occurred when selecting campaign search term: {e}")

    def select_sp_campaign_search_term_by_parent_asin(self, parent_asin,depository):
        try:
            conn = self.conn
            query = f"""
SELECT
    b.parent_asins,
    a.searchTerm,
    a.keyword,
    a.keywordBid,
    a.adGroupName,
    a.adGroupId,
    a.matchType,
    a.campaignName,
    a.campaignId,
    SUM(CASE WHEN a.date BETWEEN DATE_SUB(CURDATE()- INTERVAL 1 DAY - INTERVAL 1 DAY, INTERVAL 29 day) AND DATE_SUB(CURDATE()- INTERVAL 1 DAY, INTERVAL 1 DAY) THEN a.clicks ELSE 0 END) AS total_clicks_30d,
    SUM(CASE WHEN a.date BETWEEN DATE_SUB(CURDATE()- INTERVAL 1 DAY - INTERVAL 1 DAY, INTERVAL 6 DAY) AND DATE_SUB(CURDATE()- INTERVAL 1 DAY, INTERVAL 1 DAY) THEN a.clicks ELSE 0 END) AS total_clicks_7d,
    SUM(CASE WHEN a.date = CURDATE()- INTERVAL 1 DAY - INTERVAL 2 DAY THEN a.clicks ELSE 0 END) AS total_clicks_yesterday,
    SUM(CASE WHEN a.date BETWEEN DATE_SUB(CURDATE()- INTERVAL 1 DAY - INTERVAL 1 DAY, INTERVAL 29 day) AND DATE_SUB(CURDATE()- INTERVAL 1 DAY, INTERVAL 1 DAY) THEN a.sales14d ELSE 0 END) AS total_sales14d_30d,
    SUM(CASE WHEN a.date BETWEEN DATE_SUB(CURDATE()- INTERVAL 1 DAY - INTERVAL 1 DAY, INTERVAL 6 DAY) AND DATE_SUB(CURDATE()- INTERVAL 1 DAY, INTERVAL 1 DAY) THEN a.sales14d ELSE 0 END) AS total_sales14d_7d,
    SUM(CASE WHEN a.date = CURDATE()- INTERVAL 1 DAY - INTERVAL 2 DAY THEN a.sales14d ELSE 0 END) AS total_sales14d_yesterday,
    SUM(CASE WHEN a.date BETWEEN DATE_SUB(CURDATE()- INTERVAL 1 DAY - INTERVAL 1 DAY, INTERVAL 29 day) AND DATE_SUB(CURDATE()- INTERVAL 1 DAY, INTERVAL 1 DAY) THEN a.cost ELSE 0 END) AS total_cost_30d,
    SUM(CASE WHEN a.date BETWEEN DATE_SUB(CURDATE()- INTERVAL 1 DAY - INTERVAL 1 DAY, INTERVAL 6 DAY) AND DATE_SUB(CURDATE()- INTERVAL 1 DAY, INTERVAL 1 DAY) THEN a.cost ELSE 0 END) AS total_cost_7d,
    SUM(CASE WHEN a.date = CURDATE()- INTERVAL 1 DAY - INTERVAL 2 DAY THEN a.cost ELSE 0 END) AS total_cost_yesterday,
    SUM(CASE WHEN a.date BETWEEN DATE_SUB(CURDATE()- INTERVAL 1 DAY - INTERVAL 1 DAY, INTERVAL 29 day) AND DATE_SUB(CURDATE()- INTERVAL 1 DAY, INTERVAL 1 DAY) THEN a.cost ELSE 0 END) / SUM(CASE WHEN a.date BETWEEN DATE_SUB(CURDATE()- INTERVAL 1 DAY - INTERVAL 1 DAY, INTERVAL 29 day) AND DATE_SUB(CURDATE()- INTERVAL 1 DAY, INTERVAL 1 DAY) THEN a.sales14d ELSE 0 END) AS ACOS_30d,
    SUM(CASE WHEN a.date BETWEEN DATE_SUB(CURDATE()- INTERVAL 1 DAY - INTERVAL 1 DAY, INTERVAL 6 DAY) AND DATE_SUB(CURDATE()- INTERVAL 1 DAY, INTERVAL 1 DAY) THEN a.cost ELSE 0 END) / SUM(CASE WHEN a.date BETWEEN DATE_SUB(CURDATE()- INTERVAL 1 DAY - INTERVAL 1 DAY, INTERVAL 6 DAY) AND DATE_SUB(CURDATE()- INTERVAL 1 DAY, INTERVAL 1 DAY) THEN a.sales14d ELSE 0 END) AS ACOS_7d,
    SUM(CASE WHEN a.date = CURDATE()- INTERVAL 1 DAY - INTERVAL 2 DAY THEN a.cost ELSE 0 END) / SUM(CASE WHEN a.date = CURDATE()- INTERVAL 1 DAY - INTERVAL 2 DAY THEN a.sales14d ELSE 0 END)  AS ACOS_yesterday,
    SUM(CASE WHEN a.date BETWEEN DATE_SUB(CURDATE()- INTERVAL 1 DAY - INTERVAL 1 DAY, INTERVAL 29 day) AND DATE_SUB(CURDATE()- INTERVAL 1 DAY, INTERVAL 1 DAY) THEN a.purchases7d ELSE 0 END) AS ORDER_1m,
    SUM(CASE WHEN a.date BETWEEN DATE_SUB(CURDATE()- INTERVAL 1 DAY - INTERVAL 1 DAY, INTERVAL 6 day) AND DATE_SUB(CURDATE()- INTERVAL 1 DAY, INTERVAL 1 DAY) THEN a.purchases7d ELSE 0 END) AS ORDER_7d

FROM
    amazon_search_term_reports_sp a
JOIN
    (	SELECT
	parent_asins,
	campaignId
FROM
	amazon_advertised_product_reports_sp t1
	JOIN amazon_product_info_extended t2 ON t2.asin = t1.advertisedAsin
WHERE
	t1.market = '{self.market}'
	AND t2.market = '{depository}'
GROUP BY
	campaignId
HAVING
	TRIM(parent_asins) <> ''
	AND parent_asins IS NOT NULL
    ) b ON a.campaignId = b.campaignId
WHERE
    a.date BETWEEN DATE_SUB(CURDATE()- INTERVAL 1 DAY, INTERVAL 30 DAY) AND CURDATE()- INTERVAL 1 DAY- INTERVAL 1 DAY
    AND a.market = '{self.market}'
    AND b.parent_asins = '{parent_asin}'
    AND NOT (a.searchTerm LIKE 'b0%' AND LENGTH(a.searchTerm) = 10) -- 添加排除条件
		AND a.matchType IN ('TARGETING_EXPRESSION_PREDEFINED')
GROUP BY
    a.adGroupName,
    a.campaignName,
    a.keyword,
    a.searchTerm,
    a.matchType
ORDER BY
    a.adGroupName,
    a.campaignName,
    a.keyword,
    a.searchTerm;

                    """.format(self.market)
            df = pd.read_sql(query, con=conn)
            if df.empty:
                print("No search_term")
                return None
            else:
                # Define criteria for filtering
                # Criteria 1: Sales in the last 7 days > 0 and ACOS in the last 7 days <= 0.24
                criteria1 = (df['total_sales14d_7d'] > 0) & (df['ACOS_7d'] <= 0.24)

                # Criteria 2: Orders in the last 30 days >= 2 and average ACOS in the last 30 days <= 0.24
                criteria2 = (df['ORDER_1m'] >= 2) & (df['ACOS_30d'] <= 0.24)

                # Apply filters
                filtered_df = df[criteria1 | criteria2]

                if filtered_df.empty:
                    print("No search_term matching the criteria")
                    return None
                else:
                    print("select campaignId success")
                    return filtered_df['searchTerm'].tolist()

        except Exception as e:
            print(f"Error occurred when selecting campaign search term: {e}")

    def select_sp_delete_keyword(self):
        try:
            conn = self.conn
            query = f"""
SELECT
        market,
        campaignId,
        adGroupId,
        keywordId,
        keywordText,
        matchType,
        state,
        bid
FROM
        amazon_keywords_list_sp
WHERE
        market = '{self.market}'
        AND state = 'PAUSED'
        AND keywordText NOT IN ( '(_targeting_auto_)' )
        AND campaignId IN (
        SELECT DISTINCT
                campaignId
        FROM
                amazon_keywords_list_sp
        WHERE
                market = '{self.market}'
                AND state IN ( 'ENABLED', 'PAUSED' )
                AND keywordText NOT IN ( '(_targeting_auto_)' )
                AND extendedData_servingStatus NOT IN ( 'CAMPAIGN_PAUSED', 'AD_GROUP_PAUSED' )
        GROUP BY
                campaignId,
                adGroupId
        HAVING
                count( keywordId )> 800
        )
            """
            df = pd.read_sql(query, con=conn)
            if df.empty:
                print("No delete_keyword")
            else:
                print("select sp delete_keyword success")
                return df["keywordId"].tolist()
        except Exception as e:
            print(f"Error occurred when select_sp_delete_keyword: {e}")

    def select_sp_keyword_count(self, campaignId, adGroupId, keywordText, matchType):
        try:
            conn = self.conn
            query = f"""
SELECT COUNT(*) AS count FROM amazon_keywords_list_sp
WHERE campaignId = "{int(campaignId)}" AND adGroupId = "{int(adGroupId)}" AND keywordText = "{keywordText}" AND matchType = "{matchType}"
            """
            df = pd.read_sql(query, con=conn)
            if df.empty:
                print("No keyword")
            else:
                print("select sp keyword success")
                return df.loc[0,'count']
        except Exception as e:
            print(f"Error occurred when select_sp_keyword_count: {e}")

    def select_sp_target_count(self, campaignId, adGroupId, asin):
        try:
            conn = self.conn
            query = f"""
SELECT COUNT(*) AS count FROM amazon_targets_list_sp
WHERE campaignId = "{int(campaignId)}" AND adGroupId = "{int(adGroupId)}" AND expression LIKE "%{asin}%"
            """
            df = pd.read_sql(query, con=conn)
            if df.empty:
                print("No target")
            else:
                print("select_sp_target_count success")
                return df.loc[0,'count']
        except Exception as e:
            print(f"Error occurred when select_sp_target_count: {e}")
# api = DbSpTools('OutdoorMaster')
# #res = api.select_sd_campaign_name("FR",'M06')
# # #res = api.select_sp_product_asin("IT",'FR','B0CHRYCWPG')
# # res = api.select_sp_campaign_name('FR',"DeepBI_0514_M35_ASIN")
# res = api.select_product_sku_by_asin('FR','DE',['800810-EU'])
# #res = api.select_sp_campaign_search_term('US','M100')
# print(res)
#L17
