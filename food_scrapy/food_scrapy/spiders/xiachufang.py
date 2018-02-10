# -*- coding: utf-8 -*-
import scrapy
import datetime, socket
from ..items import FoodScrapyItem, NutritionItem, RecipeStepItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose


class XiachufangSpider(scrapy.Spider):
    ''' this is a xiachufang spider, it mainly scrapes the recipe. '''
    
    name = 'xiachufang'
    allowed_domains = ['xiachufang.com']
    start_urls = ['http://www.xiachufang.com/recipe/1086136/', ]
    
    def parse(self, response):
        """ This function parses a xiachufang page.
        @url http://www.xiachufang.com/recipe/1086136/
        @returns items 1
        @scrapes name cook steps cover_img rate_score ingredients
        @scrapes url project spider server date
        """
        recipe_name = response.xpath('//h1[@itemprop="name"]/text()').extract()[0].strip()
        
        # ----------- parse the recipe -----------
        
        l1 = ItemLoader(item=FoodScrapyItem(), response=response)
        # - prime fields -
        l1.add_xpath('cover_img', '//div/div/img/@src')
        l1.add_xpath('cook', '//span[@itemprop="name"]/text()')
        l1.add_xpath('rate_score', '//span[@itemprop="ratingValue"]/text()')
        l1.add_xpath('name', '//h1[@itemprop="name"]/text()', MapCompose(str.strip))
        l1.add_xpath('brief', '//div[@itemprop="description"]/text()', MapCompose(str.strip))
        # - housekeeping fields -
        l1.add_value('url', response.url)
        l1.add_value('project', self.settings.get('BOT_NAME'))
        l1.add_value('spider', self.name)
        l1.add_value('server', socket.gethostname())
        l1.add_value('date', str(datetime.datetime.now()))
        
        yield l1.load_item()
        
        # ----------- parse the nutrition -----------
        
        nutrition = response.xpath('//div[@class="ings"]//tr')
        for n in nutrition:
            l2 = ItemLoader(item=NutritionItem(), response=response)
            n_val = n.xpath('td[2]/text()').extract()[0].strip()
            n_name = n.xpath('td[1]/a/text()').extract()[0].strip() if n.xpath('td[1]/a/text()').extract() else \
                n.xpath('td[1]/text()').extract()[0].strip()
            l2.add_value('name', n_name)
            l2.add_value('val', n_val)
            l2.add_value('recipe', recipe_name)
            
            yield l2.load_item()
        
        # ----------- parse the recipe steps ---------
        
        steps = response.xpath('//div[@class="steps"]//li')
        for i, s in enumerate(steps):
            l3 = ItemLoader(item=RecipeStepItem(), response=response)
            l3.add_value('name', s.xpath('p/text()').extract()[0])
            l3.add_value('image_url', s.xpath('img/@src').extract()[0])
            l3.add_value('step_order', i + 1)
            l3.add_value('recipe', recipe_name)
            
            yield l3.load_item()
