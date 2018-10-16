#!/usr/bin/env python
#-*-coding: utf-8 -*-
"""
@version: 0.1
@author:linyl
@file: liaoxuefeng.py
@time: 2018/10/9 16:31
"""
from bs4 import BeautifulSoup

from base_spider import *

class LiaoxuefengSpider(BaseSpider):
    """
    爬取廖雪峰Python教程
    """

    def parse_menu(self, response):
        """
        解析目录结构，获取所有URL目录列表
        :param response: 爬虫返回的response对象
        :return: url生成器
        """
        soup = BeautifulSoup(response, 'html.parser')
        menu_tag = soup.find_all(class_='uk-nav uk-nav-side')[1]
        for a in menu_tag.find_all('a', class_='x-wiki-index-item'):
            url = a.get('href')
            if not url.startswith('http'):
                url = ''.join([self.domain, url])
            yield url

    def parse_body(self, reponse):
        """
        解析正文
        :param response: 爬虫返回的response对象
        :return: 返回处理后的html文本
        """
        try:
            soup = BeautifulSoup(reponse, 'html.parser')
            body = soup.find_all(class_='x-wiki-content x-main-content')[0]

            # 加入标题，居中显示
            title = soup.find('h4').get_text()
            center_tag = soup.new_tag('cneter')
            title_tag = soup.new_tag('h1')
            title_tag.string = title
            center_tag.insert(1, title_tag)
            body.insert(1, center_tag)

            html = str(body)
            # body中img标签的src相对路径改成绝对路径
            pattern = "(<img .*?src=\")(.*?)(\")"

            def func(m):
                if not m.group(2).startswith('http'):
                    rtn = "".join([m.group(1), self.domain, m.group(2), m.group(3)])
                    return rtn
                else:
                    return "".join([m.group(1), m.group(2), m.group(3)])
            html = re.compile(pattern).sub(func, html)
            html = html_template.format(content=html)
            return html
        except:
            logging.error("解析错误", exc_info=True)

if __name__ == '__main__':
    static_url = 'https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000'
    spider = LiaoxuefengSpider('廖雪峰的Python3',static_url)
    spider.run()

