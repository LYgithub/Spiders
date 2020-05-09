# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join

from LaGou.tools import common


class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # ID TableName DirectionType Url  (方向 大、小)
    # Company (公司)  Position(职位) Salary (薪资) Experience (经验)Education (学历)JobType (工作类型)
    # Describe (概述)
    ID = scrapy.Field()
    TableName = scrapy.Field()

    Url = scrapy.Field()
    DirectionType = scrapy.Field()
    Company = scrapy.Field()

    Position = scrapy.Field()
    Salary_min = scrapy.Field()
    Salary_max = scrapy.Field()
    Experience = scrapy.Field(
        input_processor=MapCompose(common.delete_Experience))

    Education = scrapy.Field(
        input_processor=MapCompose(common.delete_Xie))
    JobType = scrapy.Field()

    JobDescribe = scrapy.Field(
        input_processor=MapCompose(common.get_str_selecter)
    )


class ArticleLoader(ItemLoader):
    default_output_processor = TakeFirst()
