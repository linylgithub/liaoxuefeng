#!/usr/bin/env python
#-*-coding: utf-8 -*-
"""
@version: 0.1
@author:linyl
@file: html_parser.py
@time: 2018/10/14 12:54
"""
import re
import urlparse

from bs4 import BeautifulSoup


class HTMLParser(object):

    def parser(self, page_url, content):
        soup = BeautifulSoup(content, 'html.parser')
        ip_data_list = self.get_ip_list(soup)
        new_urls = self.get_new_urls(page_url, soup)
        return ip_data_list, new_urls

    def get_ip_datas(self, html):
        ip_list = []
        ip_re = re.compile(r'(?<=<td>)([\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3})')
        port_re = re.compile(r'(?<=<td>)([\d]{2,5})(?=</td>)')
        ips = re.findall(ip_re,str(html))
        ports = re.findall(port_re,str(html))
        for i in range(len(ips)):
            temp = ips[i] + ':' + ports[i]
            ip_list.append(temp)
        return ip_list

    def get_ip_list(self, soup):
        ip_list = []
        ips = soup.find_all('td', text=re.compile(r'[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}'))
        ports = soup.find_all('td', text=re.compile(r'[\s]+[\d]{2,5}[\s]+'))
        if len(ips) == len(ports):
            for i in range(len(ips)):
                ip = str(ips[i].get_text()).strip('\t|\n')
                port = str(ports[i].get_text()).strip('\t|\n')
                temp = ip + ':' + port
                ip_list.append(temp)
        return ip_list

    def get_new_urls(self, page_url, soup):
        new_urls = set()
        links = soup.find_all('a', href=re.compile(r'index_\d+\.html'))
        for link in links:
            new_url = link['href']
            new_full_url = urlparse.urljoin(page_url, new_url)
            new_urls.add(new_full_url)
        return new_urls
