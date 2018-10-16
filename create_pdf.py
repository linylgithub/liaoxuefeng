#!/usr/bin/env python
#-*-coding: utf-8 -*-
"""
@version: 0.1
@author:linyl
@file: create_pdf.py
@time: 2018/10/14 17:21
"""
import os

import pdfkit

# options = {
#            'page-size': 'Letter',
#             'margin-top': '0.75in',
#             'margin-right': '0.75in',
#             'margin-bottom': '0.75in',
#             'margin-left': '0.75in',
#             'encoding': "UTF-8",
#             'custom-header': [
#                 ('Accept-Encoding', 'gzip')
#             ],
#             'cookie': [
#                 ('cookie-name1', 'cookie-value1'),
#                 ('cookie-name2', 'cookie-value2'),
#             ],
#             'outline-depth': 10,
#         }
htmls = []
for root, dirsm, files in os.walk('.'):
    files = sorted(files, key=lambda x:os.path.getctime(os.path.join(root, x)))
    for file in files:
        if os.path.splitext(file)[1] == '.html':
            htmls.append(file)

name = '廖雪峰的python3'

# pdfkit.from_url(htmls, name + '.pdf', options=options)
pdfkit.from_url(htmls, name + '.pdf')