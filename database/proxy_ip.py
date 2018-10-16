#!/usr/bin/env python
#-*-coding: utf-8 -*-
"""
@version: 0.1
@author:linyl
@file: proxy_ip.py
@time: 2018/10/11 12:04
"""

from sqlalchemy import Column, BigInteger, String, Table, Integer

from connect import *


# 创建表格，初始化数据库
user = Table('user', metadata,
             Column('id', BigInteger, primary_key=True),
             Column('name', String(32), nullable=False),
             Column('password', String(128), nullable=False)
             )

proxy_ip = Table('proxy_ip', metadata,
             Column('id', BigInteger, primary_key=True),
             Column('protocol', String(16), nullable=False, default='https'),
             Column('ip_host', String(64), nullable=False),
             Column('status', String(32), nullable=False, default='normal'),
             Column('count', Integer, nullable=False, default=0)
             )

if __name__ == '__main__':
    metadata.create_all()