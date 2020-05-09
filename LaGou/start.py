#
# -*- coding: utf-8 -*-
# start.py 
# Created by MacBook Air PyCharm on 2020/3/27 10:31 上午 
# Copyright © 2020 LiYang. All rights reserved.
#

from scrapy import cmdline
import time


cmdline.execute('scrapy crawl LaGouSpider1_5'.split(" "))
# time.sleep(130)
cmdline.execute('scrapy crawl LaGouSpider1_6'.split(" "))
# time.sleep(130)
cmdline.execute('scrapy crawl LaGouSpider1_7'.split(" "))
# cmdline.execute('scrapy crawl test'.split(" "))