# -*- coding: utf-8 -*-

''' 这个爬虫用于为下厨房爬虫新增的字段'''

import json
import scrapy
from celery_app import r, app
from ..items import PatchItem
from front.models import Recipe
from scrapy import Request
from django.core.exceptions import ObjectDoesNotExist

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class XiachufangpathSpider(scrapy.Spider):
    name = 'xiachufangpatch'
    handle_httpstatus_list = [404, 502]
    fid_begin_flag = r.get('fid_begin_flag').decode('utf8')  # 爬取起始点
    allowed_domains = ['xiachufang.com']
    start_urls = ['http://m.xiachufang.com/recipe/%s/' % fid_begin_flag]
    
    def parse(self, response):
        
        item = PatchItem()
        try:
            stars = response.xpath('//div[@class="cooked"]//span').re('(\d+) 人做过')[0]
        except IndexError:
            stars = 0
        
        fid = self.fid_begin_flag
        item['fid'] = fid
        item['stars'] = stars
        
        v = json.dumps(dict(item))
        patch_xiachufang.delay(v)
        
        self.fid_begin_flag = int(self.fid_begin_flag) - 1
        next_recipe_url = 'http://m.xiachufang.com/recipe/%s/' % self.fid_begin_flag
        yield Request(next_recipe_url, errback=self.errback_patch, callback=self.parse)
    
    def errback_patch(self, failure):
        if failure.check(TimeoutError):
            print('-----------------Timeout Error ---------------')


@app.task(name='food_scrapy.spiders.xiachufangpatch.patch_xiachufang')
def patch_xiachufang(v):
    print('start to patch the spider')
    infos = json.loads(v)
    fid = infos.get('fid')
    print('the fid is %s' % fid)
    try:
        recipe_obj = Recipe.objects.get(fid=fid)
        print('get the object')
        recipe_obj.stars = infos.get('stars')
        
        recipe_obj.save()
        if recipe_obj.stars == infos.get('stars') and recipe_obj.stars != 0:
            print('succeed updated stars number')
    
    except ObjectDoesNotExist:
        pass
