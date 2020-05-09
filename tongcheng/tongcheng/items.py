# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
from tongcheng.utils import common
from scrapy.loader import ItemLoader


class TongchengItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # response.url+"\t"+money+"\t"+ jiGou+paiLiang+
    # "\t"+bianSuxiang+"\t"+youHao
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    money = scrapy.Field()
    jiGou = scrapy.Field(
        input_processor=MapCompose(common.get_message)
    )
    paiLiang = scrapy.Field(
        input_processor=MapCompose(common.get_message)
    )
    bianSuxiang = scrapy.Field(
        input_processor=MapCompose(common.get_message)
    )
    youHao = scrapy.Field(
        input_processor=MapCompose(common.get_message)
    )
    image_url = scrapy.Field(
        output_processor=MapCompose(lambda x: [x])
    )
    image_path = scrapy.Field()


# 自定义 ItemLoader 解决全部字段 取第一个
class ArticleLoader(ItemLoader):
    default_output_processor = TakeFirst()

