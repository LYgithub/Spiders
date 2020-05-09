#
# -*- coding: utf-8 -*-
# base.py
# Created by MacBook Air PyCharm on 2020/3/19 3:43 下午
# Copyright © 2020 LiYang. All rights reserved.
#
import datetime
import hashlib
import re

NUMBER = 0
NUMBER2 = 0


def get_message(str_test):
    s = re.match(r".*</span>(.*)</li>", str_test, re.S)
    str_test = s[1]
    s1 = ""
    while s1 != str_test:
        s1 = str_test
        s = re.match(r".*?(<.*?>).*?(<.*?>).*?", str_test)
        if s is not None:
            str_test = str_test.replace(s[1], "")
            str_test = str_test.replace(s[2], "")
            str_test = str_test.replace("'", "")
            str_test = str_test.replace("'", "")
    s = re.match(".*?(<a .*?>).*?", str_test)
    if s is not None:
        str_test = str_test.replace(s[1], "")

    return str_test


def get_md5(url):
    # str 表示 Unicode
    if isinstance(url, str):
        url = url.encode('utf-8')
    m = hashlib.md5()
    # Unicode 不能进行 md5
    m.update(url)
    return m.hexdigest()


def get_data(time):
    try:
        time = datetime.datetime.strftime(time, "%Y/%m%/d").date()
    except Exception as e:
        time = datetime.datetime.now()
        print(e)
    finally:
        return time


