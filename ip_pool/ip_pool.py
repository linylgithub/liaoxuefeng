#!/usr/bin/env python
#-*-coding: utf-8 -*-
"""
@version: 0.1
@author:linyl
@file: ip_pool.py
@time: 2018/10/9 18:04
"""
import random
import time
import urllib2
from bs4 import BeautifulSoup
import re
from database.connect import *
from database.model.proxy_ip import ProxyIP
from user_agents import user_agents


class IPPool(object):

    def add_ips(self, session, protocol, ip_list):
        for ip_host in ip_list:
            self.add_ip_host(session, protocol, ip_host)

    def add_ip_host(self, session, protocol, ip_host):
        id = ProxyIP.add(session, protocol, ip_host, status='normal')
        return id

    @classmethod
    def update_ip_status(cls, session, ip_host):
        suc = ProxyIP.update_status(session, ip_host)
        return suc

    @classmethod
    def get_ip_pools(cls, session):
        ip_list = []
        ip_host_list = ProxyIP.get_status_ip_list(session)
        for ip_host in ip_host_list:
            protocol = ip_host['protocol']
            ip = ip_host['ip_host']
            ip_list.append('%s://%s'%(protocol, ip))
        return ip_list

    def test_proxy(ip_host, target_url, session):
        """
        测试代理链接是否有效，
        :param ip_host:
        :return:
        """
        if 'https' in ip_host:
            px = urllib2.ProxyHandler({'https': ip_host})
        else:
            px = urllib2.ProxyHandler({'http': ip_host})
        opener = urllib2.build_opener(px)
        urllib2.install_opener(opener)

        try:
            req = urllib2.Request(target_url)
            req.add_header('User-Agent',random.choice(user_agents))
            resp = urllib2.urlopen(req)
            if not resp:
                ProxyIP.update_status(session, ip_host)
            return True

        except Exception as e:
            print('%s,%s'%(ip_host,e))
            ProxyIP.update_status(session, ip_host)
            return False

if __name__ == '__main__':
    pass

