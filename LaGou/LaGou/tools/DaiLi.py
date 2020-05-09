#
# -*- coding: utf-8 -*-
# DaiLi.py 
# Created by MacBook Air PyCharm on 2020/3/23 6:46 下午 
# Copyright © 2020 LiYang. All rights reserved.
#
# 代理获取
# 返回元组 ('5d2265e7751bc9247088597ef9b3638d', 'http', '183.146.213.157', '80')
# 列表 []
# 字典 {}
# 元组 ()
import requests
from bs4 import BeautifulSoup
import re
from Boss.util import Proxy_SQL
from Boss.util import common


class DaiLi(object):
    def __init__(self):
        self.url = "https://ip.jiangxianli.com/?page="
        self.connect = Proxy_SQL.SQLConnect()

    def download_proxy(self, page):
        response = requests.get(self.url, page)
        soup = BeautifulSoup(response.text, 'lxml')
        td_list = soup.find_all('tr')
        for i in td_list:
            s = re.match('<tr><td>(.*?)</td><td>(.*?)</td>.*(HTTP*).*', str(i), re.S)
            if s is not None:
                proxy = s.group(3).lower() + "://" + s.group(1) + ":" + s.group(2)
                if self.check(proxy):
                    data = {
                        'IP_ID': common.get_md5(proxy),
                        'LeiXing': s.group(3).lower(),
                        'IP': s.group(1),
                        'Port': s.group(2)
                    }
                    # print(data)
                    print('📝📝🤑🤑🤑:' + proxy)
                    self.connect.dowmload(data=data)
                else:
                    print('❎❎😟😟😟:' + proxy)

        # # 下一页
        # next = soup.find_all(class_=r'layui-laypage-next')
        # print(next)

    def main(self):
        print('===================     start crawl!     ===================')
        for i in range(1, 10):
            print('===================     page:'+str(i)+'     ===================')
            self.download_proxy(self.url + str(i) + "&anonymity=2")
        print('===================     finish crawl!     ===================')

    def check(self, proxy):
        proxies = {
            'http': proxy
        }
        try:
            response = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=(1, 1))
            if re.match('{.*}$', response.text, re.S) is not None:
                return True
            else:
                return False
        except Exception as e:
            print('❌:' + str(e))

    def get_proxy(self):
        print('===================     start get IP!     ===================')
        while True:
            sql_ = Proxy_SQL.SQLConnect()
            ip_ = sql_.put_one()
            # 无
            if ip_ is None:
                Proxy_ = DaiLi()
                Proxy_.main()
            # 有
            else:
                ip = ip_[1] + "://" + ip_[2] + ":" + ip_[3]
                if self.check(ip):
                    print('✅✅😘😘😘：' + ip)
                    print('===================     finish get IP!     ===================')
                    return ip
                else:
                    print('❎❎😟😟😟' + ip)
                    # print(ip_)
                    # print('😟😟😟😟😟😟')


if __name__ == '__main__':
    test = DaiLi()
    print(test.get_proxy())
