# -*- coding: utf-8 -*-
import scrapy


class XiachufangSpider(scrapy.Spider):
    name = 'xiachufang'
    allowed_domains = ['xiachufang.com']
    start_urls = ['http://xiachufang.com/']

    def parse(self, response):
        pass
