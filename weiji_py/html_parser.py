#
# /Users/mac/PycharmProjects 
# -*- coding: utf-8 -*-
# @Time    : 2017/8/23 下午10:13
# @Author  : Liyang
# @Site    : 
# @File    : html_parser.py
# @Software: PyCharm
#
#
# 网页管理器
# 包括判断是否URL为照片和判断一个URL是否被爬取函数

import re


class HtmlParse(object):

    def __init__(self):
        self.old_all_url = set()

    def has_url(self, url1):
        if url1 in self.old_all_url and self.is_jpg(url1):
            return False
        else:
            self.old_all_url.add(url1)
            return True

    def is_jpg(self, url):
        return re.search(r"\.(jpg|JPG)$", url["href"])
