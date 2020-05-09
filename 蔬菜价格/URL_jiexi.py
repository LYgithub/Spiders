#
# /Users/mac/PycharmProjects 
# -*- coding: utf-8 -*-
# @Time    : 2017/8/23 上午11:21
# @Author  : Liyang
# @Site    : 
# @File    : URL_jiexi.py
# @Software: PyCharm
#
#
#HTML解析器
"""
通过对URL下的HTML生成bs对象
来查找有用的URL，对进行下一步的爬取做准备
"""

from  bs4 import BeautifulSoup
import  re
import urllib.parse
from urllib.request import urlopen

class JieXi():
    def __init__(self):
        self.data = []
        self.new_url = ''
    def URL_jiexi(self,new_url,html_cont = None):         #解析URL
        try:
            url = urlopen(new_url).read().decode("utf-8")
            soup =BeautifulSoup (
                url,
                "html.parser",
                from_encoding="utf-8"
            )

            #获取url
            # < a href = / price / t2 > 2 < / a >
            # new_urls = soup.find_all("a",target = "_blank",href = re.compile("^/item/[A-Za-z]+$"))

            #
            # for url in new_urls:
            #     url["href"] = "https://baike.baidu.com" + url["href"]
            #     #print(url["href"])
            # self.new_url = new_urls
            # return new_urls

            new_urls = soup.find_all("a", href=re.compile(r"/price/t\d"))
            for url in new_urls:
                url["href"] = "http://www.shucai123.com/price.php" + url["href"]
            self.new_url = new_urls
            return new_urls
        except:
            print("file")





