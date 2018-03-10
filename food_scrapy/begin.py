#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' 此脚本用于在Pycharm中单步调试scrapy 和 启动spider'''
import os
from scrapy import cmdline


# 此处需要指定虚拟环境里的scrapy

scrapy_path = '../.env/bin/scrapy'

execuete_spider = "%s crawl manual" % scrapy_path
cmdline.execute(execuete_spider.split())
