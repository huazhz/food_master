# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin
from ..items import RecipeItem
from scrapy.loader import ItemLoader
from scrapy.http import Request
from scrapy.loader.processors import MapCompose
from celery_app import r


class XiachufangSpider(scrapy.Spider):
    ''' this is a xiachufang spider, it mainly scrapes the recipe. '''
    
    name = 'manual'
    allowed_domains = ['xiachufang.com']
    start_urls = ['http://www.xiachufang.com/category/', ]
    
    def parse(self, response):
        '''
        从顶级目录向下解析所有子目录
        '''
        self.log(response.status)
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
            # yield Request(urljoin(response.url, link), callback=self.parse_item)
            if not r.sismember('urlset', link):
                r.sadd('urlset', link)
                yield Request(urljoin(response.url, link), callback=self.parse_item)
            else:
                return None
        
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
            try:
                usage = n.xpath('td[2]/text()').extract()[0].strip()
            except:
                usage = "暂无"
            try:
                ingredient = n.xpath('td[1]/a/text()').extract()[0].strip() \
                    if n.xpath('td[1]/a/text()').extract() \
                    else n.xpath('td[1]/text()').extract()[0].strip()
            except:
                ingredient = "暂无"
            
            dict_ingre['usage'] = usage
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
            try:
                dict_steps['step_detail'] = s.xpath('p/text()').extract()[0]
            except:
                dict_steps['step_detail'] = '暂无'
            try:
                dict_steps['image_url'] = s.xpath('img/@src').extract()[0] if s.xpath('img/@src').extract()[0] else \
                    response.xpath('//img[@class="recipe-menu-cover"]/@src').extract()[i - 1]
            except IndexError:
                dict_steps['image_url'] = '暂无'
            list_steps.append(dict_steps)
        
        # ----------- parse the recipe -----------
        
        item = RecipeItem()
        try:
            item['fid'] = response.url.split('/')[-2]
        except:
            item['fid'] = '暂无'
        try:
            item['cover_img'] = response.xpath('//div/div/img/@src').extract()[0]
        except:
            item['cover_img'] = '暂无'
        try:
            item['cook'] = response.xpath('//span[@itemprop="name"]/text()').extract()[0]
        except:
            item['cook'] = '暂无'
        try:
            item['rate_score'] = response.xpath('//span[@itemprop="ratingValue"]/text()').extract()[0]
        except:
            item['rate_score'] = '暂无'
        try:
            item['name'] = response.xpath('//h1[@itemprop="name"]/text()').extract()[0].strip()
        except:
            item['name'] = '暂无'
        try:
            item['brief'] = response.xpath('//div[@itemprop="description"]/text()').extract()[0].strip()
        except:
            item['brief'] = '暂无'
        
        item['recipe_ingredients'] = list_ingre
        item['steps'] = list_steps
        
        author_url = response.xpath('//div[@class="author"]/a/@href').extract()[0]
        yield Request(url='http://www.xiachufang.com' + author_url, meta={'item': item},
                      callback=self.parse_author)
    
    def parse_author(self, response):
        
        item = response.meta['item']
        
        try:
            name = response.xpath('//h1/text()').extract()[0].strip()
        except:
            name = '暂无'
        try:
            gender = response.xpath('//div[@class="gray-font"]//span[1]/text()')[0].extract()
            if gender not in ['男', '女']:
                gender = '暂无'
        except:
            gender = '暂无'
        try:
            brief_intro = response.xpath('//div[contains(@class,"people-base-desc")][1]/text()')[0].extract().strip()
        except:
            brief_intro = '暂无'
        email = ''
        mobile = ''
        password = ''
        md5_password = ''
        is_fake = 1
        join_ip = ''
        cook_dict = dict(name=name, gender=gender, brief_intro=brief_intro, email=email, mobile=mobile,
                         password=password, md5_password=md5_password, is_fake=is_fake, join_ip=join_ip)
        item['cook'] = cook_dict
        
        print('he')
        
        yield item
