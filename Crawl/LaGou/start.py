#
# -*- coding: utf-8 -*-
# start.py 
# Created by MacBook Air PyCharm on 2020/3/27 10:31 上午 
# Copyright © 2020 LiYang. All rights reserved.
#
from scrapy import cmdline


cmdline.execute('scrapy crawl LaGouSpider'.split(" "))
# cmdline.execute('scrapy crawl test'.split(" "))