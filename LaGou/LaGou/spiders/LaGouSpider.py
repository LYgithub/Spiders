# -*- coding: utf-8 -*-
import scrapy
from pydispatch import dispatcher
from scrapy import signals
from selenium import webdriver
from scrapy.http import Request
from LaGou.tools import random_ua
from LaGou.tools import common
from LaGou.tools.Chrome_Tools import Chrome_Tool
from LaGou.items import ArticleLoader
from urllib import parse
import time
import re
from LaGou import items


class LagouspiderSpider(scrapy.Spider):
    name = 'LaGouSpider'
    allowed_domains = ['www.lagou.com/beijing']
    start_urls = ['https://www.lagou.com/beijing/']


    def __init__(self):
        # 信号量
        self.chrome = Chrome_Tool()
        super().__init__()
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)
        self.number = 1

    # 重启浏览器后需要重新 获取网页
    # self.chrome.get_page(url)
    def set_chrome(self):
        self.chrome.__del__()
        self.chrome.__init__()

    def spider_closed(self):
        self.chrome.__del__()

    # 解析首页
    def parse(self, response):
        selectors_titles = response.xpath('//div[@class="mainNavs"]/div[1]/div[2]/dl')
        for title in selectors_titles:
            TableName = title.xpath('dt/span/text()').get()
            print("========  " + TableName + "   ========")
            self.logger.info("========  " + TableName + "   ========")
            for i in title.xpath('dd//a'):
                DirectionType = i.xpath('h3/text()').get()
                url = i.xpath('@href').get()
                self.logger.info("%s %s %s",DirectionType, ":", url)
                print(DirectionType, ":", url)
                # 列表页请求
                time.sleep(10)
                yield Request(url=url,
                              meta={'TableName': TableName,
                                    'DirectionType': DirectionType,
                                    'Key':True},
                              callback=self.parse_detial,
                              encoding='utf8',
                              dont_filter=True)



    # 解析列表页
    def parse_detial(self, response):
        print("列表页：", response.url)
        try:
            TableName = response.meta.get('TableName',"其他")
            DirectionType = response.meta.get('DirectionType',"x")
            self.logger.info("✅列表页: %s : %s : %s",TableName,DirectionType,response.url)

            ## 解析网页 通过循环获取职位Url 交给 详情页解析函数解析
            # //ul[@class="item_con_list"]/li[2]
            selectors = response.xpath('//ul[@class="item_con_list"]/li')

            for selector in selectors:
                Company_url = selector.xpath('div[1]/div[2]/div/a/@href').get()
                Company = selector.xpath('div[1]/div[2]/div/a/text()').get()
                Company = Company + '('+Company_url+')'
                url = selector.xpath('div[1]/div[1]/div/a/@href').get()
                s = re.match('(^https://.*?\.html)\?show=.*',url)
                url = s.group(1)
                time.sleep(30)
                yield Request(url=url,
                              meta={
                                  'Key':False,
                                  'TableName': TableName,
                                  'DirectionType': DirectionType,
                                  'Company': Company,
                              },
                              callback=self.parse_detial_message,
                              encoding='utf8',
                              dont_filter=True)
        except Exception as e:
            self.logger.info("❌❌解析列表页[Error]：%s : %s",response.url, e)
            print("❌❌解析列表页[Error]：%s : %s",response.url, e)
        # 传递点击事件   获取URL
        try:
            i = 0
            while not self.chrome.find("//div[@class='item_con_pager']/div/a[@class='page_no pager_next_disabled']"):
                i = i + 1
                time.sleep(30)
                yield Request(url=parse.urljoin(response.url, str(i)),
                              meta={
                                  'Key':True,
                                  'TableName': TableName,
                                  'DirectionType': DirectionType,
                              },
                              callback=self.parse_detial,
                              encoding='utf8',
                              dont_filter=True)
        except Exception as e:
            self.logger.info("❌❌列表下一页[Error]: %s %s", response.url, e)
            print("❌❌列表下一页[Error]: %s %s", response.url, e)

    # 解析详情页 ？？
    def parse_detial_message(self, response):
        print("详情页：", response.url)
        if response.status != 200:
            time.sleep(60)
            self.logger.info("❌❌详情页获取失败！[error]: %s %s",response.url, response.status)
            print("❌❌详情页获取失败！[error]: %s %s",response.url, response.status)
            yield Request(url=parse.urljoin(response.url, str(i)),
                          meta={
                              'Key':True,
                              'TableName': response.meta.get("TableName","其他"),
                              'DirectionType': response.meta.get("DirectionType",'X')
                          },
                          callback=self.parse_detial,
                          encoding='utf8',
                          dont_filter=True)

        # ID TableName DirectionType Url  (方向 大、小)
        # Company (公司)  Position(职位) Salary (薪资) Experience (经验)Education (学历)JobType (工作类型)
        # JobDescribe (概述)
        try:
            item_loader =ArticleLoader(item=items.LagouItem(), response=response)

            TableName = response.meta.get('TableName', '其他')
            DirectionType = response.meta.get('DirectionType', '不知')
            Company = response.meta.get('Company', '不知')

            item_loader.add_value('ID',common.get_md5(TableName+DirectionType+Company+response.url))

            item_loader.add_value('TableName', TableName)
            item_loader.add_value('DirectionType', DirectionType)
            item_loader.add_value('Url', response.url)

            item_loader.add_value('Company', Company)
            item_loader.add_xpath('Position', '//h1/text()')

            Salary = response.xpath('//div[@class="position-content-l"]/dd/h3/span[1]/text()').get()


            if re.match('(.*k)\-(.*k)', Salary):
                s = re.match('(.*)\-(.*)', Salary)
                item_loader.add_value('Salary_min', s.group(1))
                item_loader.add_value('Salary_max', s.group(2))
            else:
                item_loader.add_value('Salary_min', Salary)
                item_loader.add_value('Salary_max', '-')

            item_loader.add_xpath('Experience', '//div[@class="position-content-l"]/dd/h3/span[3]/text()') # 经验5-10年 /
            item_loader.add_xpath('Education', '//div[@class="position-content-l"]/dd/h3/span[4]/text()') # 本科及以上 /
            item_loader.add_xpath('JobType', '//div[@class="position-content-l"]/dd/h3/span[5]/text()') # 全职
            # item_loader.add_xpath('JobDescribe', '//*[@id="job_detail"]/dd[2]//text()')

            str_ = ""
            Describe = response.xpath('//*[@id="job_detail"]/dd[2]//text()')
            for i in Describe:
                str_ += i.get()

            item_loader.add_value('JobDescribe', str_)

            item = item_loader.load_item()
            print(item)
            yield item
        except Exception as e:
            self.logger.info('⭕️⭕️详情页信息获取失败: %s %s',response.url)
            print('⭕️⭕️详情页信息获取失败: %s %s',response.url)



