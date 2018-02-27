#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
此脚本用于在Pycharm中单步调试scrapy
'''

from scrapy import cmdline

cmdline.execute("scrapy crawl manual".split())
