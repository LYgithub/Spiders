# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import pymysql.cursors
import logging
from twisted.enterprise import adbapi


class MySQLTwistedPipline(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            database=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            password=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )
        # adbapi会将数据库写入变成异步
        dbpool = adbapi.ConnectionPool('pymysql', **dbparms)
        return cls(dbpool)

    # 使用Twisted将MySQL插入变成异步
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 添加异步错误处理函数
        query.addErrback(self.handle_error)
        return item

    def handle_error(self, failure):
        print(failure)

    # ID TableName Url DirectionType  (方向 大、小)
    # Company (公司)  Position(职位) Salary (薪资) Experience (经验)Education (学历)JobType (工作类型)
    # Describe (概述)
    def do_insert(self, cursor, item):
        inster_sql = """
                insert into %s(ID,Url,DirectionType,Company,Position,Salary_min,Salary_max,Experience,Education,JobType,JobDescribe)
                values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')
            """%(
        item['TableName'],
        item['ID'],
        item['Url'],
        item['DirectionType'],
        item['Company'],
        item['Position'],
        item['Salary_min'],
        item['Salary_max'],
        item['Experience'],
        item['Education'],
        item['JobType'],
        item['JobDescribe']
    )
        try:
            cursor.execute(inster_sql)
            print("📝📝📝✅✅")
        except Exception as e:
            logging.info("❌❌ %s",inster_sql)

