#
# -*- coding: utf-8 -*-
# login.py 
# Created by MacBook Air PyCharm on 2020/3/22 10:46 上午 
# Copyright © 2020 LiYang. All rights reserved.
#
import re
import scrapy
import json


class loginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['car.58che.com']
    start_urls = ['https://car.58che.com/series/s5.html']
    headers = {
        'User-Agent': ''
    }

    def parse(self, response):
        #
        yield scrapy.Request(response.url, callback=self.parse_detial, dont_filter=True)

    def parse_detial (self):
        # 解析真正的网页
        pass

    def start_requests(self):
        return [scrapy.Request('post_url', headers=self.headers, callback=self.login)]

    def login(self, response):
        # 获取 _xsrf
        response_text = response.text
        _xsrf = re.match('<>(.*?)<.*>', response_text, re.S)
        post_data = {
            '_xsrf': _xsrf.group(1),
            'user': 'user',
            'passwed': '***'
        }

        # 完成表单提交
        return [scrapy.FormRequest(
            url='https://passport.58.com/58/login/pc/dologin',
            formdata=post_data,
            headers=self.headers,
            # 同步操作  传递函数对象   否则返回函数返回值
            callback=self.check_login
        )]

    def check_login(self, response):
        # 验证是否登录成功
        json_text = json.loads(response.text)
        if 'msg' in json_text and json_text['msg'] == '登录成功':
            print('登录成功！')
        else:
            print(json_text['mst'])

        for url in self.start_urls:
            # yield self.make_requests_from_url(url)
            # 默认回到 parse
            yield scrapy.Request(url, dont_filter=True, headers=self.headers)
        pass








