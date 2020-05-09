#
# /Users/mac/PycharmProjects 
# -*- coding: utf-8 -*-
# @Time    : 2017/8/23 下午12:01
# @Author  : Liyang
# @Site    : 
# @File    : URL_downloader.py
# @Software: PyCharm
#
#
#网页下载器
"""
主要就是下载所爬取的URL ，以及英文字条在百度百科下的简单阐述
"""
from bs4 import BeautifulSoup
import urllib.request
class HTML_downloader(object):
    def __init__(self):
        self.out = open("url.html", "w")
        print("""<html><meta http-equiv="Content Type" content="text/html" charset="utf-8" />""", file=self.out)

    def URL_downloader(self,str1,str2):

        #print("<table>" , file = self.out )
        self.out.write('<table><br>')
        #"""<a href = "{}" target = "_blank">{}</a><br>""".format(str["href"],str.get_txt())
        print("""<a href = "{}" target = "_blank">{}</a><br>---------------------------------------------""".format(str1,str2), file=self.out)
        print("</table>",file = self.out)


    def data_down(self,w):
        a = urllib.request.urlopen(w)

        test = BeautifulSoup(
            a,
            "html.parser",
            from_encoding="utf-8"
        )
        print(w, "\n",file=self.out)

        #print("""< div class ="para" label-module="para" > 构成是中国汉语里的词汇，意思是形成；造成。 < / div >""",file = ai)
        # <div class="para" label-module="para">图像处理(image processing)，用计算机对图像进行分析，以达到所需结果的技术。又称影像处理。图像处理一般指数字图像处理。数字图像是指用工业相机、摄像机、扫描仪等设备经过拍摄得到的一个大的二维数组，该数组的元素称为像素，其值称为灰度值。图像处理技术一般包括图像压缩，增强和复原，匹配、描述和识别3个部分。 </div>
        # <td>
        #                 <a href='/price/辣椒/'>辣椒</a>
        #             </td>
        #             <td title="价格美丽！上市量少！">巨无霸优质：
        #                 <b class="fred">3.2元/斤</b> &nbsp;
        #                 <p style="color:#669900; line-height:18px;">价格美丽！上市量少！</p>
        #             </td>
        #

        # wendang = test.find("div",class_ = "para")
        wendang = test.find("a",)
        #for i in wendang:
        print("<strong><br>",wendang.get_text(),"\n</strong><br>\n", file=self.out )

    def __del__(self):
        print("</html>", file=self.out)
        self.out.close()





