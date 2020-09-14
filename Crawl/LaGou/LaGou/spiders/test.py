# -*- coding: utf-8 -*-
import scrapy


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['httpbin.org/ip']
    start_urls = ['http://httpbin.org/user-agent']

    def parse(self, response):
        print(response)
        print(response.status)
        self.logger.info('Parse function called on %s', response.url)
        self.logger.error('Error %s', response.url)

        self.logger.error("❌❌解析列表页: %s %s", response.url,response.url)
