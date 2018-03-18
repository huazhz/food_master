# -*- coding: utf-8 -*-

''' 这个爬虫用于为下厨房爬虫新增的字段'''

import json
import scrapy
from celery_app import r
from ..items import PatchItem
from front.models import Recipe
from scrapy import Request
from twisted.internet.error import TimeoutError, TCPTimedOutError
from patch_crawler import patch_xiachufang

fids = []
for rec in Recipe.objects.all():
    fids.append(rec.fid)

print(fids)


class XiachufangpathSpider(scrapy.Spider):
    name = 'xiachufangpatch'
    handle_httpstatus_list = [404, 502]
    
    r.set('begin', 0)
    begin = int(r.get('begin'))
    nowfid = fids[begin]
    allowed_domains = ['xiachufang.com']
    start_urls = ['http://m.xiachufang.com/recipe/%s/' % nowfid]
    
    def parse(self, response):
        
        item = PatchItem()
        try:
            stars = response.xpath('//div[@class="cooked"]//span').re('(\d+) 人做过')[0]
        except IndexError:
            stars = 0
        
        nowfid = fids[self.begin]
        item['fid'] = nowfid
        item['stars'] = stars
        
        v = json.dumps(dict(item))
        patch_xiachufang.delay(v)
        
        self.begin += 1
        nextfid = fids[int(self.begin)]
        next_recipe_url = 'http://m.xiachufang.com/recipe/%s/' % nextfid
        r.set('begin', self.begin)
        
        yield Request(next_recipe_url, errback=self.errback_patch, callback=self.parse)
    
    def errback_patch(self, failure):
        if failure.check(TimeoutError):
            print('-----------------Timeout Error ---------------')
