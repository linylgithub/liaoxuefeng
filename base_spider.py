#!/usr/bin/env python
#-*-coding: utf-8 -*-
"""
@version: 0.1
@author:linyl
@file: base_spider.py
@time: 2018/10/6 16:21
"""

import logging
import os
import random
import re
import time

from urlparse import urlparse
import pdfkit
import requests
import urllib2
from ip_pool import ip_pool
from database.connect import *
from ip_pool import html_downloader

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
{content}
</body>
</html>
"""

class BaseSpider(object):
    """
    爬虫基类，所有的爬虫都应该继承此类
    """
    name = None

    def __init__(self, name, start_url):
        """
        初始化
        :param name: 将要被保存为PDF的文件名称
        :param start_url: 爬虫入口URl
        """
        self.name = name
        self.start_url = start_url
        self.domain = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(self.start_url))
        self.session = Session()
        self.ip_pools = ip_pool.IPPool.get_ip_pools(self.session)
        self.html_downloader = html_downloader.HtmlDownLoader()

    @staticmethod
    def request(url, ip_host, **kwargs):
        """
        网络请求，返回response对象
        :param url:
        :param kwargs:
        :return:
        """
        if 'https' in ip_host:
            px = urllib2.ProxyHandler({'https': ip_host})
        else:
            px = urllib2.ProxyHandler({'http': ip_host})

        opener = urllib2.build_opener(px)
        request = urllib2.Request(url)
        request.add_header("user-agent","Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36")
        response = urllib2.urlopen(request)
        return response

    def parse_menu(self, response):
        """
        从response中解析出所有目录的URL链接
        :param response:
        :return:
        """
        raise NotImplementedError

    def parse_body(self, reponse):
        """
        解析正文，由子类实现
        :param reponse:
        :return:
        """
        raise NotImplementedError

    def run(self):
        start = time.time()
        options = {
           'page-size': 'Letter',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
            'cookie': [
                ('cookie-name1', 'cookie-value1'),
                ('cookie-name2', 'cookie-value2'),
            ],
            'outline-depth': 10,
        }
        htmls = []
        ip_host = random.choice(self.ip_pools)
        menu = self.html_downloader.download_by_proxy(self.start_url, ip_host)

        while not menu:
            ip_pool.IPPool.update_ip_status(self.session, ip_host.split('://')[1])
            ip_host = random.choice(self.ip_pools)
            menu = self.html_downloader.download_by_proxy(self.start_url, ip_host)
        if not menu:
            raise Exception('没有足够可用代理ip！')

        for index, url in enumerate(self.parse_menu(menu)):
            ip_host = random.choice(self.ip_pools)
            body = self.html_downloader.download_by_proxy(url,ip_host)
            while not body:
                ip_pool.IPPool.update_ip_status(self.session, ip_host.split('://')[1])
                ip_host = random.choice(self.ip_pools)
                body = self.html_downloader.download_by_proxy(url,ip_host)

            if not body:
                raise Exception('没有足够可用代理ip！')

            html = self.parse_body(body)
            f_name = '.'.join([str(index), "html"])
            with open(f_name, 'wb') as f:
                f.write(html)
            htmls.append(f_name)

        pdfkit.from_url(htmls, self.name + '.pdf', options=options)
        for html in htmls:
            os.remove(html)
        total_time = time.time() - start
        print('总共耗时：%f 秒'%total_time)



