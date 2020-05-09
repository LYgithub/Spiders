#
# -*- coding: utf-8 -*-
# common.py 
# Created by MacBook Air PyCharm on 2020/3/29 4:21 下午 
# Copyright © 2020 LiYang. All rights reserved.
#
import hashlib
import re


def get_md5(url_):
    # str 表示 Unicode
    if isinstance(url_, str):
        url_ = url_.encode('utf-8')
    m = hashlib.md5()
    # Unicode 不能进行 md5
    m.update(url_)
    return m.hexdigest()


def get_str_selecter(list_):
    s = ""
    for i in list_:
        s += i
    return s


def delete_Experience(str_):
    try:
        s = re.search(r'经验(.*) /', str_, re.S)
        return s.group(1)
    except Exception as e:
        print("❌❌格式化数据失败：", str_, e)
        return str_
    

def delete_Xie(str_):
    try:
        s = re.match(r'(.*) /', str_, re.S)
        return s.group(1)
    except Exception as e:
        print("❌❌删除斜线失败：", str_, e)
        return str_


if __name__ == "__main__":
    x = delete_Experience('经验5-10年 /')
    print(x)
    print(delete_Xie(x))
