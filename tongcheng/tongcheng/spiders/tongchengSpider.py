# -*- coding: utf-8 -*-
import scrapy
import re
from urllib import parse
from scrapy.http import Request
from tongcheng.utils import common
from tongcheng import items
from scrapy.loader import ItemLoader
from tongcheng.items import ArticleLoader


class TongchengspiderSpider(scrapy.Spider):
    name = 'tongchengSpider'
    allowed_domains = ['car.58che.com']
    start_urls = ['https://car.58che.com/series/s5.html']

    def parse(self, response):
        try:
            # 处理列表页
            selectors = response.xpath('//ul[@class="s_list clearfix"]//li/div/a[1]')
            for selector in selectors:
                # url = parse.urljoin(response.url, selector.xpath('./@href').get())
                # image_url = parse.urljoin(response.url, selector.xpath('./img/@src').get())
                url = parse.urljoin(response.url, selector.css("::attr(href)").get())
                image_url = parse.urljoin(response.url, selector.css('img::attr(src)').get())
                print(url)
                print(image_url)
                print(common.NUMBER)
                common.NUMBER += 1
                yield scrapy.http.Request(url=url, meta={'image_url':image_url}, callback=self.parse_detial,  dont_filter=True)

            # 下一页
            post_url = response.xpath("body/div[@id='page_num']/a[@class='next']/@href").get()
            yield Request(url= parse.urljoin(response.url, post_url),callback=self.parse)
        except:
            print("\033[43m Error:" + response.url)


    def parse_detial(self, response):
        # article_item = items.TongchengItem()/

        # 处理详情页
        # 本地参考价：7.38-10.28万
        # 厂商指导价：7.38-10.28万
        # 结 构：两厢车/三厢车
        # 排 量：1.5L
        # 变速箱： 手动 无级变速
        # 油 耗：5.3-5.7L
        try:
            # 如果 image_url 没有 则为 空
            front_image_url = response.meta.get('image_url', "")

            money = response.xpath('//div[@class="canshu"]/div/div/div[2]/a/em/text()').get()
            #'<li class="w132">
            #   <span>结   构：</span>
            #   <a href="//www.58che.com/2435/liangxiang/">两厢车</a>/<a href="//www.58che.com/2435/sanxiang/">三厢车</a>
            #   </li>'
            #<li class="w132">
            # <span>结   构：</span><a href="//www.58che.com/2435/liangxiang/">两厢车</a>/<a href="//www.58che.com/2435/sanxiang/">三厢车</a></li>
            jiGou = common.get_message(response.xpath('//ul[@class="canshu_list"]/li[1]').get())

            paiLiang = common.get_message(response.xpath('//ul[@class="canshu_list"]/li[2]').get())

            bianSuxiang = common.get_message(response.xpath('//ul[@class="canshu_list"]/li[3]').get())
            youHao = common.get_message(response.xpath('//ul[@class="canshu_list"]/li[4]').get())
            print(response.url+"\t"+money+"\t"+ jiGou+"\t"+paiLiang+"\t"+bianSuxiang+"\t"+youHao)
            print(common.NUMBER2)
            common.NUMBER2 += 1
            # article_item['image_url'] = [front_image_url]
            # article_item['money'] = money
            # article_item['jiGou'] = jiGou
            # article_item['paiLiang'] = paiLiang
            # article_item['bianSuxiang'] = bianSuxiang
            # article_item['youHao'] = youHao
            # article_item['url'] = response.url
            # article_item['url_object_id'] = common.get_md5(response.url)




            # item_loader = ItemLoader(item=items.TongchengItem(), response=response)
            item_loader =ArticleLoader(item=items.TongchengItem(), response=response)
            # for i in range(0,4):
            #     item_loader.add_xpath(name_list[i], '//ul[@class="canshu_list"]/li['+str(i+1)+']')
            item_loader.add_xpath('money', '//div[@class="canshu"]/div/div/div[2]/a/em/text()')
            item_loader.add_xpath('jiGou', '//ul[@class="canshu_list"]/li[1]')
            item_loader.add_xpath('paiLiang', '//ul[@class="canshu_list"]/li[2]')
            item_loader.add_xpath('bianSuxiang', '//ul[@class="canshu_list"]/li[3]')
            item_loader.add_xpath('youHao', '//ul[@class="canshu_list"]/li[4]')
            item_loader.add_value('image_url', front_image_url)
            item_loader.add_value('url_object_id', common.get_md5(response.url))
            item_loader.add_value('url', response.url)

            print(item_loader)

            article_item = item_loader.load_item()

            yield article_item
        except Exception as e:
            print("\033[43m Error:" + response.url)
            print(e)