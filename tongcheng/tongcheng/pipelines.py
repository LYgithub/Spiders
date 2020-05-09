# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os

from scrapy.pipelines.images import ImagesPipeline
import codecs
from scrapy.exporters import JsonItemExporter
import pymysql
import pymysql.cursors


class TongchengPipeline(object):
    # 接受 ITEM_PIPLINES
    # yield 过来的
    def process_item(self, item, spider):
        # 数据存储
        return item


class MySQLPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect()
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into Car(url,url_object_id,money,jieGou,paiLiang,bianSuxiang,youHao,image_url,image_path)
            values (%s, %s,%s, %s,%s, %s,%s, %s,%s)
            
        """
        self.cursor.execute(insert_sql, (item["url"], item['url_object_id'], item["money"], item["jiGou"],
                                         item["paiLiang"], item["bianSuxiang"], item["youHao"], item['image_url'],
                                         item['image_path']))
        self.conn.commit()


class JsonExporterPipline(object):
    # 调用scrapy 提供的json export 导出json文件
    def __init__(self):
        self.file = open('atricleexport.json', 'wb')
        # 实例化
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class JsonWithEncodingPipline(object):
    # 打开Json 文件
    # 自定义文件的导出
    def __init__(self):
        self.file = codecs.open('article.json', 'a', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False)+"\n"
        print(line)
        self.file.write(line)
        return item

    def spuder_closed(self, spider):
        self.file.close()


# 图片下载
class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok, value in results:
            image_path = value["path"]
        item['image_path'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'images/'+image_path)
        # ※
        return item


from twisted.enterprise import adbapi


class MySqlTwistedPipline(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        # cls 就是本身类
        # 读取setting
        # host: Host where the database server is located
        #     :param user: Username to log in as
        #     :param password: Password to use.
        #     :param database: Database to use, None to not use a particular one.
        #     :param port: MySQL port to use, default is usually OK. (default: 3306)
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            database=settings["MYSQL_DBNAME"],

            user=settings["MYSQL_USER"],
            password=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用 twisted 将mysql插入编程异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        # query.addErrback(self.handle_error)
        return item

    # 异步数据插入 adbapi
    # 异步容器 使用 pymysql 库
    def handle_error(self, failure):
        # 处理异步插入的异常
        print("Error")
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        # response.url+"\t"+money+"\t"+ jiGou+paiLiang+
        # "\t"+bianSuxiang+"\t"+youHao
        insert_sql = """
            insert into Car(url,url_object_id,money,jieGou,paiLiang,bianSuxiang,youHao,image_url,image_path)
            values (%s, %s,%s, %s,%s, %s,%s, %s,%s)
            
        """
        cursor.execute(insert_sql, (item["url"], item['url_object_id'], item["money"], item["jiGou"], item["paiLiang"],
                                    item["bianSuxiang"], item["youHao"], item['image_url'], item['image_path']))














