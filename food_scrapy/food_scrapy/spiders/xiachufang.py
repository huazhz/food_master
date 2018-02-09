# -*- coding: utf-8 -*-
import scrapy
from ..items import FoodScrapyItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose


class XiachufangSpider(scrapy.Spider):
    name = 'xiachufang'
    allowed_domains = ['xiachufang.com']
    start_urls = ['http://www.xiachufang.com/recipe/1086136/']
    
    def parse(self, response):
        ''' 解析函数 '''
        l = ItemLoader(item=FoodScrapyItem(), response=response)
        l.add_xpath('name', '//h1[@itemprop="name"]/text()', MapCompose(str.strip))
        l.add_xpath('cook', '//span[@itemprop="name"]/text()')
        l.add_xpath('brief', '//div[@itemprop="description"]/text()', MapCompose(str.strip))
        l.add_xpath('cover_img', '//div/div/img/@src')
        l.add_xpath('rate_score', '//span[@itemprop="ratingValue"]/text()')
        l.add_xpath('ingredients', '//div[@class="ings"]')
        l.add_xpath('steps', '//div[@class="steps"]')
        
        return l.load_item()
        
        # old style
        # item = FoodScrapyItem()
        # item['name'] = response.xpath('//h1[@itemprop="name"]/text()').extract()[0].strip()
        # item['cook'] = response.xpath('//span[@itemprop="name"]/text()').extract()[0].strip()
        # item['brief'] = response.xpath('//div[@itemprop="description"]/text()').extract()[0].strip()
        # item['cover_img'] = response.xpath("//div/div/img/@src").extract()[0]
        # item['rate_score'] = response.xpath('//span[@itemprop="ratingValue"]/text()').extract()[0]
        # item['ingredients'] = response.xpath('//div[@class="ings"]').extract()
        # item['steps'] = response.xpath('//div[@class="steps"]').extract()
        
        # 打印
        # self.log('rate_score: %s' % response.xpath('//span[@itemprop="ratingValue"]/text()').extract())
        # self.log('name: %s ' % response.xpath('//h1[@itemprop="name"]/text()').extract())
        # self.log('cook: %s ' % response.xpath('//span[@itemprop="name"]/text()').extract())
        # self.log('brief: %s ' % response.xpath('//div[@itemprop="description"]/text()').extract())
        # self.log('cover_img: %s' % response.xpath("//div/div/img/@src").extract())
        # self.log('ingredients: %s' % response.xpath('//div[@class="ings"]').extract())
        # self.log('steps: %s' % response.xpath('//div[@class="steps"]').extract())
        
        # return item
