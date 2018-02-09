# -*- coding: utf-8 -*-
import scrapy
from ..items import FoodScrapyItem


class XiachufangSpider(scrapy.Spider):
    name = 'xiachufang'
    allowed_domains = ['xiachufang.com']
    start_urls = ['http://www.xiachufang.com/recipe/1086136/']
    
    def parse(self, response):
        ''' 解析函数 '''
        item = FoodScrapyItem()
        item['name'] = response.xpath('//h1[@itemprop="name"]/text()').extract()[0].strip()
        item['cook'] = response.xpath('//span[@itemprop="name"]/text()').extract()[0].strip()
        item['brief'] = response.xpath('//div[@itemprop="description"]/text()').extract()[0].strip()
        item['cover_img'] = response.xpath("//div/div/img/@src").extract()[0]
        item['rate_score'] = response.xpath('//span[@itemprop="ratingValue"]/text()').extract()[0]
        item['ingredients'] = response.xpath('//div[@class="ings"]').extract()
        item['steps'] = response.xpath('//div[@class="steps"]').extract()
        #
        # 打印
        # self.log('rate_score: %s' % response.xpath('//span[@itemprop="ratingValue"]/text()').extract()[0])
        # self.log('name: %s ' % response.xpath('//h1[@itemprop="name"]/text()').extract()[0].strip())
        # self.log('cook: %s ' % response.xpath('//span[@itemprop="name"]/text()').extract()[0].strip())
        # self.log('brief: %s ' % response.xpath('//div[@itemprop="description"]/text()').extract()[0].strip())
        # self.log('cover_img: %s' % response.xpath("//div/div/img/@src").extract()[0])
        # self.log('ingredients: %s' % response.xpath('//div[@class="ings"]').extract())
        # self.log('steps: %s' % response.xpath('//div[@class="steps"]').extract())
        
        return item
