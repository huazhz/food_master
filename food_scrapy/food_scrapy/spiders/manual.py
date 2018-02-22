# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin
import datetime, socket
from ..items import RecipeItem
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
        
        # 纵向爬取菜谱页
        recipe_links = response.xpath('//a[contains(@class, "recipe")]//@href').re('/recipe/\d+/')
        for link in recipe_links:
            yield Request(urljoin(response.url, link), callback=self.parse_item)
        
        # 横向爬取下一页
        # next_page = response.xpath('//a[@class="next"]//@href').extract()[0]
        # yield Request(urljoin(response.url, next_page))
    
    def parse_item(self, response):
        """ 解析菜谱详情并生成item
        @url http://www.xiachufang.com/recipe/1086136/
        @returns items 3
        @scrapes name cook cover_img rate_score
        @scrapes url project spider server date
        @scrapes name val recipe
        @scrapes name image_url step_order recipe
        """
        recipe_name = response.xpath('//h1[@itemprop="name"]/text()').extract()[0].strip()
        
        # ----------- parse the RecipeIngredient -----------
        
        list_ingre = []
        recipe_ingredient = response.xpath('//div[@class="ings"]//tr')
        for n in recipe_ingredient:
            dict_ingre = dict()
            usage = n.xpath('td[2]/text()').extract()[0].strip()
            ingredient = n.xpath('td[1]/a/text()').extract()[0].strip() \
                if n.xpath('td[1]/a/text()').extract() \
                else n.xpath('td[1]/text()').extract()[0].strip()
            dict_ingre['usage'] = usage if usage else None
            dict_ingre['ingredient'] = ingredient
            dict_ingre['recipe'] = recipe_name
            list_ingre.append(dict_ingre)
        
        # ----------- parse the recipe steps ---------
        
        list_steps = []
        steps = response.xpath('//div[@class="steps"]//li')
        for i, s in enumerate(steps, 1):
            dict_steps = dict()
            dict_steps['step_order'] = i
            dict_steps['recipe'] = recipe_name
            dict_steps['step_detail'] = s.xpath('p/text()').extract()[0]
            try:
                dict_steps['image_url'] = s.xpath('img/@src').extract()[0] if s.xpath('img/@src').extract()[0] else \
                    response.xpath('//img[@class="recipe-menu-cover"]/@src').extract()[i - 1]
            except IndexError:
                dict_steps['image_url'] = None
            list_steps.append(dict_steps)
        
        # ----------- parse the recipe -----------
        
        l1 = ItemLoader(item=RecipeItem(), response=response)
        # - prime fields -
        l1.add_value('fid', response.url.split('/')[-2])
        l1.add_xpath('cover_img', '//div/div/img/@src')
        l1.add_xpath('cook', '//span[@itemprop="name"]/text()')
        l1.add_xpath('rate_score', '//span[@itemprop="ratingValue"]/text()')
        l1.add_xpath('name', '//h1[@itemprop="name"]/text()', MapCompose(str.strip))
        l1.add_xpath('brief', '//div[@itemprop="description"]/text()', MapCompose(str.strip))
        l1.add_value('recipe_ingredients', list_ingre)
        l1.add_value('steps', list_steps)
        
        author_url = response.xpath('//div[@class="author"]/a/@href').extract()[0]
        yield Request(url='http://www.xiachufang.com' + author_url, meta={'item': l1.load_item()},
                      callback=self.parse_author)
    
    def parse_author(self, response):
        item = response.meta['item']
        name = response.xpath('//h1/text()').extract()[0].strip()
        gender = response.xpath('//div[@class="gray-font"]//span[1]/text()')[0].extract()
        brief_intro = response.xpath('//div[contains(@class,"people-base-desc")][1]/text()')[0].extract()
        email = ''
        mobile = ''
        password = ''
        md5_password = ''
        is_fake = 1
        join_ip = ''
        cook_dict = dict(name=name, gender=gender, brief_intro=brief_intro, email=email, mobile=mobile,
                         password=password, md5_password=md5_password, is_fake=is_fake, join_ip=join_ip)
        item['cook'] = cook_dict
        
        url = response.url
        print(url)
        
        yield item
