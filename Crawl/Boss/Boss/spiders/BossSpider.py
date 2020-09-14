# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from urllib import parse
from selenium.webdriver.chrome.options import Options
# 浏览器设置

chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')



class BossMainspiderSpider(scrapy.Spider):
    name = 'BossSpider'
    allowed_domains = ['www.zhipin.com']
    start_urls = ['https://www.zhipin.com/']

    def __init__(self):
        self.browser = webdriver.Chrome(chrome_options=chrome_options)

    def parse(self, response)
        try:
            selecter = response.xpath("//div[@class='job-menu']/dl[1]/div[2]/ul")
            # for i in selecter:
            #     print(i)
            for i in selecter.xpath('./li'):
                # 获取方向
                print(i.xpath('./*/text()').get())
                # 获取该方向下的 语言
                # print(i.xpath('.//a/text()'))
                for harf in i.xpath('.//a'):
                    yield scrapy.Request(url=parse.urljoin(response.url, harf.xpath('./@href').get()),
                                         callback=self.parse_datial, dont_filter=True)
                    print(harf.xpath('./text()').get())
        except Exception as e:
            print(e)

    def parse_datial(self, response):
        print(response.url)

    # set proxy
    def set_proxy(self):
        chrome_options.add_argument('--proxy-server=https://0.0.0.0:8080')





