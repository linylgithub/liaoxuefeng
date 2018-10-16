#!/usr/bin/env python
#-*-coding: utf-8 -*-
"""
@version: 0.1
@author:linyl
@file: ip_main.py
@time: 2018/10/14 14:08
"""
import logging
import random
import time

import url_manager
import html_downloader
import html_parser
import ip_pool
from database.connect import *

class IPMain(object):

    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownLoader()
        self.parser = html_parser.HTMLParser()
        self.ip_pool = ip_pool.IPPool()
        self.session = Session()
        self.ip_pools = self.ip_pool.get_ip_pools(self.session)

    def craw(self, root_url):
        self.urls.add_new_url(root_url)
        count = 1
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                logging.info('craw %d : %s' %(count, new_url))
                print('craw %d : %s' %(count, new_url))
                if len(self.ip_pools) > 0:
                    ip_host = random.choice(self.ip_pools)
                    html_cont = self.downloader.download_by_proxy(new_url, ip_host)
                else:
                    html_cont = self.downloader.download(new_url)
                if not html_cont:
                    self.ip_pool.update_ip_status(self.session, ip_host.split('://')[1])
                    continue
                # html_cont = self.downloader.download(new_url)
                if html_cont:
                    ip_list, new_urls = self.parser.parser(new_url, html_cont)
                    self.urls.add_new_urls(new_urls)
                    self.ip_pool.add_ips(self.session, 'https', ip_list)
                    self.urls.set_old_url(new_url)
                    count += 1
                    time.sleep(1)
                else:
                    logging.error('打开页面失败')
            except Exception as e:
                logging.error(e.message)

if __name__ == '__main__':
    root_url = 'http://www.89ip.cn/index_30.html'
    main = IPMain()
    main.craw(root_url)