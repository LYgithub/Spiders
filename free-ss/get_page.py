# free-ss.site 网页解析器
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_page():
    option = Options()
    option.add_argument("--proxy-server:http://")
    browser = webdriver.Chrome()
    browser.get('https://free-ss.site/')
    print(browser.page_source)
    x = input('请输入退出信息：')
    print(x)


def get_file():
    file = open('/Users/mac/Desktop/免费上网账号/免费上网账号.html', 'r')
    page = file.read()
    return str(page)


def jiexi(page):
    soup = BeautifulSoup(
        page,
        'lxml'
    )
    return soup.find_all('tbody')[1]

if __name__ == '__main__':
    # print(get_file())
    for i in jiexi(get_file()):
        for x in i.find_all('td'):
            print(x.text)

