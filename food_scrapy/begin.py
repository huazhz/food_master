#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
此脚本用于在Pycharm中单步调试scrapy
'''
import os
from scrapy import cmdline

proj_path = os.path.dirname(os.path.dirname(__file__))
# scrapy_path = proj_path + '.env/bin/scrapy'

# 此处需要指定虚拟环境里的scrapy
scrapy_path = proj_path + 'venv/bin/scrapy'

execuete_spider = "%s crawl manual" % scrapy_path
cmdline.execute(execuete_spider.split())
