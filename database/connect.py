#!/usr/bin/env python
#-*-coding: utf-8 -*-
"""
@version: 0.1
@author:linyl
@file: connect.py
@time: 2018/10/11 11:46
"""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL = 'mysql+mysqldb://root:root123@localhost:3306/spider_proxy_ip?charset=utf8'
Base = declarative_base()

engine = create_engine(DB_URL,
                       pool_size=1,
                       max_overflow=10,
                       echo=False,
                       encoding='utf-8',
                       pool_recycle=20000)
Session = sessionmaker(bind=engine)
metadata = MetaData(bind=engine)