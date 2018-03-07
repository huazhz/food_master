# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin
from ..items import RecipeItem
from scrapy.http import Request
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
        s = set()
        recipe_links = response.xpath('//a[contains(@class, "recipe")]//@href').re('/recipe/\d+/')
        if not recipe_links:
            return None
        
        for link in recipe_links:
            if not r.sismember('visited_urlset', 'http://www.xiachufang.com' + link):
                s.add(link)
            else:
                continue
        
        # 横向爬取下一页
        try:
            next_page = response.xpath('//a[@class="next"]//@href').extract()[0]
            yield Request(urljoin(response.url, next_page), callback=self.parse_category)
        except IndexError:
            pass
        
        while len(s) > 0:
            yield Request(urljoin('http://www.xiachufang.com', s.pop()),
                          callback=self.parse_item)
    
    # def parse_category(self, response):
    #     pass
    
    def parse_item(self, response):
        """ 解析菜谱详情并生成item
        @url http://www.xiachufang.com/recipe/1086136/
        @returns items 3
        @scrapes name cook cover_img rate_score
        @scrapes url project spider server date
        @scrapes name val recipe
        @scrapes name image_url step_order recipe
        """
        
        if response.status != 200:
            return None
        
        recipe_name = response.xpath('//h1[@itemprop="name"]/text()').extract()[0].strip()
        
        # ----------- parse the RecipeIngredient -----------
        
        list_ingre = []
        recipe_ingredient = response.xpath('//div[@class="ings"]//tr')
        for n in recipe_ingredient:
            dict_ingre = dict()
            try:
                usage = n.xpath('td[2]/text()').extract()[0].strip()
            except IndexError:
                usage = "暂无"
            try:
                ingredient = n.xpath('td[1]/a/text()').extract()[0].strip() \
                    if n.xpath('td[1]/a/text()').extract() \
                    else n.xpath('td[1]/text()').extract()[0].strip()
            except IndexError:
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
            except IndexError:
                dict_steps['step_detail'] = '暂无'
            try:
                dict_steps['image_url'] = s.xpath('img/@src').extract()[0] if s.xpath('img/@src').extract()[0] else \
                    response.xpath('//img[@class="recipe-menu-cover"]/@src').extract()[i - 1]
            except IndexError:
                dict_steps['image_url'] = '暂无'
            list_steps.append(dict_steps)
        
        # ----------- parse the recipe -----------
        
        item = RecipeItem()
        
        item['url'] = response.url
        recipe_category = response.xpath('//div[@class="recipe-cats"]/a/text()').extract()
        
        # recipe_menu_list = response.xpath('//img[@class="recipe-menu-cover"]/@alt').extract()
        # recipe_menu_link_list = response.xpath('//a[contains(@class,"recipe-menu")]/@href').extract()
        
        # try:
        #     item['recipe_menu_list'] = recipe_menu_list
        # except Exception:
        #     item['recipe_menu_list'] = []
        try:
            item['category'] = recipe_category
        except IndexError:
            item['category'] = '全部'
        try:
            item['fid'] = response.url.split('/')[-2]
        except IndexError:
            item['fid'] = '暂无'
        try:
            item['cover_img'] = response.xpath('//div/div/img/@src').extract()[0]
        except IndexError:
            item['cover_img'] = '暂无'
        try:
            item['cook'] = response.xpath('//span[@itemprop="name"]/text()').extract()[0]
        except IndexError:
            item['cook'] = '暂无'
        try:
            item['rate_score'] = response.xpath('//span[@itemprop="ratingValue"]/text()').extract()[0]
        except IndexError:
            item['rate_score'] = '暂无'
        try:
            item['name'] = response.xpath('//h1[@itemprop="name"]/text()').extract()[0].strip()
        except IndexError:
            item['name'] = '暂无'
        try:
            item['brief'] = response.xpath('//div[@itemprop="description"]/text()').extract()[0].strip()
        except IndexError:
            item['brief'] = '暂无'
        
        item['recipe_ingredients'] = list_ingre
        item['steps'] = list_steps
        try:
            author_url = response.xpath('//div[@class="author"]/a/@href').extract()[0]
            yield Request(url='http://www.xiachufang.com' + author_url, meta={'item': item},
                          callback=self.parse_author)
        except IndexError:
            return None
    
    def parse_author(self, response):
        
        item = response.meta['item']
        
        try:
            name = response.xpath('//h1/text()').extract()[0].strip()
        except IndexError:
            name = '暂无'
        try:
            gender = response.xpath('//div[@class="gray-font"]//span[1]/text()')[0].extract()
            if gender not in ['男', '女']:
                gender = '暂无'
        except IndexError:
            gender = '暂无'
        try:
            brief_intro = response.xpath('//div[contains(@class,"people-base-desc")][1]/text()')[0].extract().strip()
        except IndexError:
            brief_intro = '暂无'
        
        is_fake = 1
        email = '暂无'
        mobile = '暂无'
        join_ip = '暂无'
        password = '暂无'
        md5_password = '暂无'
        
        cook_dict = dict(name=name, gender=gender, brief_intro=brief_intro, email=email, mobile=mobile,
                         password=password, md5_password=md5_password, is_fake=is_fake, join_ip=join_ip)
        item['cook'] = cook_dict
        
        yield item
