#
# -*- coding: utf-8 -*-
# zhihu.py 
# Created by MacBook Air PyCharm on 2020/3/21 4:29 下午 
# Copyright © 2020 LiYang. All rights reserved.
#

import requests
import http.cookiejar as cookielib

session = requests.session()

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/80.0.3987.149 Safari/537.36'
}
response = requests.get("https://www.zhihu.com", headers=headers)

print(response)
cookies = response.cookies

print(cookies)
# print(response.text)

post_url = 'https://www.zhihu.com'
post_data = {
    'key': 'value'
}
response = requests.post(post_url, data=post_data, headers=headers)
response1 = session.post(post_url, data=post_data, headers=headers)

session.cookies = cookielib.LWPCookieJar(filename='cook.txt')
session.cookies.save()

try:
    session.cookies.load(ignore_discard=True)
except:
    print('cookies 加载失败')

print(response)
print(response1)
