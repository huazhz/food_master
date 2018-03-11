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
    
    # def start_requests(self):
    #     start_url = 'http://m.xiachufang.com/recipe/%s/' % self.fid_begin_flag  # brutal force 策略
    #     headers = {'referer': 'http://m.xiachufang.com/',
    #                "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
    #                "Accept-Encoding": "gzip, deflate",
    #                "Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6",
    #                "Cache-Control": "no-cache",
    #                "Connection": "keep-alive",
    #                "Cookie": "gr_user_id=a99acc51-83d6-4100-8e85-0c61e8ac87c9; __utmz=177678124.1520252214.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga=GA1.2.715750840.1520252214; Hm_lvt_ecd4feb5c351cc02583045a5813b5142=1520085303,1520146073,1520252214,1520614524; __utmc=177678124; _gid=GA1.2.179269571.1520654731; gr_session_id_da48e7b9eb89482489897fc1e45e98b6=d2a5d16e-f77a-422e-8980-8c3223cfa243; gr_session_id_8187ff886f0929da=c8ae0751-3632-4778-a506-5ba5d5f5903a; Hm_lpvt_ecd4feb5c351cc02583045a5813b5142=1520752413; __utma=177678124.715750840.1520252214.1520738827.1520752414.24; __utmb=177678124.1.10.1520752414; _gat=1",
    #                "Host": "s2.cdn.xiachufang.com",
    #                "Pragma": "no-cache",
    #                "Referer": "http://m.xiachufang.com/",
    #                # "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1}"
    #                }
    #     yield scrapy.Request(url=start_url, headers=headers, callback=self.parse)
    
    def parse(self, response):
        item = PatchItem()
        try:
            stars = response.xpath('//div[@class="cooked"]//span').re('(\d+) 人做过')[0]
        except IndexError:
            stars = 0
        brief = response.xpath('//p[contains(@class,"recipe-desc")]/text()').extract() or ['暂无']
        fid = self.fid_begin_flag
        item['fid'] = fid
        item['stars'] = stars
        item['brief'] = brief
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
        recipe_obj.brief = infos.get('brief')
        recipe_obj.save()
        if recipe_obj.stars == infos.get('stars'):
            print('succeed')
    
    except ObjectDoesNotExist:
        pass
