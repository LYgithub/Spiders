#
# -*- coding: utf-8 -*-
# common.py 
# Created by MacBook Air PyCharm on 2020/3/24 9:25 下午 
# Copyright © 2020 LiYang. All rights reserved.
#
import hashlib


def get_md5(url):
    # str 表示 Unicode
    if isinstance(url, str):
        url = url.encode('utf-8')
    m = hashlib.md5()
    # Unicode 不能进行 md5
    m.update(url)
    return m.hexdigest()