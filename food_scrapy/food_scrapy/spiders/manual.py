# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin
import datetime, socket
from ..items import FoodScrapyItem, NutritionItem, RecipeStepItem
from scrapy.loader import ItemLoader
from scrapy.http import Request
from scrapy.loader.processors import MapCompose


class XiachufangSpider(scrapy.Spider):
    ''' this is a xiachufang spider, it mainly scrapes the recipe. '''
    
    name = 'manual'
    allowed_domains = ['xiachufang.com']
    start_urls = ['http://www.xiachufang.com/category/', ]
    
    def parse(self, response):
        '''
        从顶级目录向下解析所有子目录
        '''
        category_links = response.xpath('//a[(contains(@href, category))]/@href').re('/category/\d+/')
        for url in category_links:
            yield Request(urljoin(response.url, url), callback=self.parse_category)
    
    def parse_category(self, response):
        '''
        在category级别进行横向抽取和纵向抽取
        '''
        # 横向爬取下一页
        recipe_next_link = response.xpath('//a[@class="next"]//@href').extract()[0]
        yield Request(urljoin(response.url, recipe_next_link))
        
        # 纵向爬取菜谱页
        recipe_links = response.xpath('//a[contains(@class, "recipe")]//@href').re('/recipe/\d+/')
        for link in recipe_links:
            yield Request(urljoin(response.url, link), callback=self.parse_item)
    
    def parse_item(self, response):
        """ This function parses a xiachufang page.
        @url http://www.xiachufang.com/recipe/1086136/
        @returns items 3
        @scrapes name cook cover_img rate_score
        @scrapes url project spider server date
        @scrapes name val recipe
        @scrapes name image_url step_order recipe
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
        l1.add_value('spider', self.name)
        l1.add_value('server', socket.gethostname())
        l1.add_value('date', str(datetime.datetime.now()))
        l1.add_value('project', self.settings.get('BOT_NAME'))
        
        yield l1.load_item()
        
        # ----------- parse the nutrition -----------
        
        nutrition = response.xpath('//div[@class="ings"]//tr')
        for n in nutrition:
            l2 = ItemLoader(item=NutritionItem(), response=response)
            n_val = n.xpath('td[2]/text()').extract()[0].strip()
            n_name = n.xpath('td[1]/a/text()').extract()[0].strip() \
                if n.xpath('td[1]/a/text()').extract() \
                else n.xpath('td[1]/text()').extract()[0].strip()
            l2.add_value('val', n_val)
            l2.add_value('name', n_name)
            l2.add_value('recipe', recipe_name)
            
            yield l2.load_item()
        
        # ----------- parse the recipe steps ---------
        
        steps = response.xpath('//div[@class="steps"]//li')
        for i, s in enumerate(steps, 1):
            l3 = ItemLoader(item=RecipeStepItem(), response=response)
            l3.add_value('step_order', i)
            l3.add_value('recipe', recipe_name)
            l3.add_value('name', s.xpath('p/text()').extract()[0])
            l3.add_value('image_url', s.xpath('img/@src').extract()[0])
            
            yield l3.load_item()
