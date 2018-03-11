# -*- coding: utf-8 -*-

''' 这个爬虫用于为下厨房爬虫新增的字段'''

import scrapy
from celery_app import r
from ..items import PatchItem
from scrapy import Request


class XiachufangpathSpider(scrapy.Spider):
    name = 'xiachufangpatch'
    handle_httpstatus_list = [404]
    fid_begin_flag = r.get('fid_begin_flag').decode('utf8')  # 爬取起始点
    allowed_domains = ['xiachufang.com']
    start_urls = ['http://m.xiachufang.com/recipe/%s/' % fid_begin_flag]  # brutal force 策略
    
    def parse(self, response):
        item = PatchItem()
        try:
            stars = response.xpath('//div[@class="cooked"]//span').re('(\d+) 人做过')[0]
        except IndexError:
            stars = 0
        brief = response.xpath('//p[contains(@class,"recipe-desc")]/text()').extract() or ['暂无']
        item['stars'] = stars
        item['brief'] = brief
        yield item
        
        self.fid_begin_flag = int(self.fid_begin_flag) - 1
        next_recipe = 'http://m.xiachufang.com/recipe/%s/' % self.fid_begin_flag
        yield Request(next_recipe, callback=self.parse)
