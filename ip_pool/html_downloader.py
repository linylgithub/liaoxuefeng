#!/usr/bin/env python
#-*-coding: utf-8 -*-
"""
@version: 0.1
@author:linyl
@file: html_downloader.py
@time: 2018/10/12 17:51
"""

import urllib2
import random
from user_agents import *


class HtmlDownLoader(object):

    def download(self, new_url):
        """
        下载页面
        :param new_url:
        :return: 返回页面
        """
        if new_url is None:
            return None
        request = urllib2.Request(new_url)
        request.add_header("user-agent", random.choice(user_agents))
        response = urllib2.urlopen(request)

        if response.getcode() != 200:
            return None
        return response.read()

    def download_by_proxy(self, new_url, ip_host):
        """
        通过代理服务器下载页面
        :param new_url:
        :param ip_host:
        :return:
        """
        if new_url is None:
            return None
        if 'https' in ip_host:
            proxy_support = urllib2.ProxyHandler({'https': ip_host})
        else:
            proxy_support = urllib2.ProxyHandler({'http': ip_host})
        opener = urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)
        request = urllib2.Request(new_url)
        request.add_header("user-agent", random.choice(user_agents))
        try:
            response = urllib2.urlopen(request,timeout=5)
            if response.getcode() != 200:
                return None
            return response.read()
        except Exception as e:
            return None


