#
# -*- coding: utf-8 -*-
# Chrome_Tools.py
# Created by MacBook Air PyCharm on 2020/3/27 11:39 上午 
# Copyright © 2020 LiYang. All rights reserved.
#
# 随机设置请求头
# 使用   先创建对象 -> 更换 UA  -> del 再创建一个对象
# 点击  click()
#
from selenium import webdriver
from LaGou.tools import random_ua
from selenium.webdriver.chrome.options import Options


class Chrome_Tool:
    def __init__(self):
        self.options = Options()
        self.options.add_argument('user-agent=' + random_ua.get_UA())
        # 设置 IP代理
        # 无界面请求
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--disable-dev-shm-usage')
        self.browser = webdriver.Chrome(options=self.options)

    # 第一步
    def get_page(self):
        return self.browser.page_source

    def set_url(self, url):
        self.browser.get(url=url)

    # 点击事件  -> 用 JavaScript
    def click(self, xpath):
        try:
            elenment = self.browser.find_element_by_xpath(xpath=xpath)
            self.browser.execute_script("arguments[0].click();", elenment)
            return self.browser.page_source
        except Exception as e:
            print("❌❌点击失败：", self.browser.current_url,e)
            return None

    def reset(self):
        self.__del__()
        self.__init__()

    def find(self, xpath):
        try:
            return self.browser.find_element_by_xpath(xpath=xpath)
        except Exception:
            # print(e)
            return None

    def __del__(self):
        self.browser.quit()




