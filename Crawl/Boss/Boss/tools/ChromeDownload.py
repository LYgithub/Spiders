#
# -*- coding: utf-8 -*-
# ChromeDownload.py 
# Created by MacBook Air PyCharm on 2020/3/22 4:59 下午 
# Copyright © 2020 LiYang. All rights reserved.
#
from scrapy.http import HtmlResponse


class ChromeMinddleware(object):

    def __init__(self):
        pass

    def process_request(self, request, spider):
        #print(spider.browser.current_url)
        return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding='utf8', request=request)