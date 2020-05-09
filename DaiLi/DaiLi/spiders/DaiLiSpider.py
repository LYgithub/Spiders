# -*- coding: utf-8 -*-
import scrapy


class DailispiderSpider(scrapy.Spider):
    name = 'DaiLiSpider'
    allowed_domains = ['ip.jiangxianli.com']
    start_urls = ['https://ip.jiangxianli.com/']

    def parse(self, response):
        print(response)
        pass
