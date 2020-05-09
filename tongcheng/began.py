#
# -*- coding: utf-8 -*-
# began.py 
# Created by MacBook Air PyCharm on 2020/3/19 3:13 下午 
# Copyright © 2020 LiYang. All rights reserved.
#
from datetime import datetime

from scrapy import cmdline


cmdline.execute("scrapy crawl tongchengSpider".split())
# cmdline.execute("scrapy crawl login".split())
# print(datetime(2020, 5, 3, 8, 21, 51, 105573) - datetime(2020, 5, 3, 8, 20, 54, 334193))
