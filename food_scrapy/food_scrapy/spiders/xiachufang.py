# -*- coding: utf-8 -*-

import scrapy
from ..items import RecipeItem, RecepeListItem
from scrapy.http import Request
from celery_app import r


class XiachufangSpider(scrapy.Spider):
    ''' this is a xiachufang spider, it mainly scrapes the recipe. '''
    name = 'xiachufang'
    handle_httpstatus_list = [404, 502]
    
    fid_begin_flag = r.get('fid_begin_flag').decode('utf8')  # 爬取起始点
    allowed_domains = ['xiachufang.com']
    
    # start_urls = ['http://www.xiachufang.com/category/']  # 遍历策略
    # not_scrapied_numer = 0
    # scrapied_numer = 0
    # start_page = 1
    #
    def start_requests(self):
        meta = {'dont_redirect': True, "handle_httpstatus_list": [302, 301]}
        start_url = 'http://www.xiachufang.com/recipe/%s/' % self.fid_begin_flag  # brutal force 策略
        yield Request(url=start_url,
                      meta=meta,
                      callback=self.parse)
    
    def parse(self, response):
        '''
        从顶级目录向下解析所有子目录
        '''
        self.log(response.status)
        
        # --------------------------------brutal force 策略 -------------------------------------------------------------
        
        # brutal force 策略
        self.fid_begin_flag = int(self.fid_begin_flag) + 1
        r.set('fid_begin_flag', self.fid_begin_flag)
        new_url = 'http://www.xiachufang.com/recipe/%s/' % r.get('fid_begin_flag').decode('utf8')
        
        if not r.sismember('visited_urlset', response.url):
            print('------------- this url has been scraped ---------------')
            if response.status == 200:
                yield Request(response.url, callback=self.parse_recipe, dont_filter=True)
            if response.status == 302:
                yield Request(response.url.replace('m.', ''), callback=self.parse_recipe, dont_filter=True)
        else:
            print('------------- this url has been scraped ---------------')
        
        yield Request(new_url, callback=self.parse, dont_filter=True)
    
    #     # ------------------------------- 原有逻辑，从顶部目录开始向下遍历 ------------------------------------------------------
    #
    #     recent_urls = response.xpath('//a//@hre').re('/explore/\w*/?')  # ['/explore/', '/explore/rising/', ...]
    #     category_links = response.xpath('//a[(contains(@href, category))]/@href').re('/category/\d+/')
    #
    #     # 爬取最近页
    #     for url in recent_urls:
    #         yield Request('http://www.xiachufang.com' + url + '?page=%s' % self.start_page,
    #                       callback=self.parse_category)
    #
    #     # 爬取所有页
    #     for url in category_links:
    #         yield Request(('http://www.xiachufang.com' + url[:-1] + '?page=%s' % self.start_page),
    #                       callback=self.parse_category)
    #
    # def parse_category(self, response):
    #     '''
    #     在category级别进行横向抽取和纵向抽取
    #     '''
    #     # 纵向爬取
    #     recipe_links = response.xpath('//a[contains(@class, "recipe")]//@href').re('/recipe/\d+/')
    #     if not recipe_links:
    #         return None
    #
    #     for link in recipe_links:
    #         if not r.sismember('visited_urlset', 'http://www.xiachufang.com' + link):
    #             self.not_scrapied_numer += 1
    #             self.log('this recipe has not been scrapied, link is %s' % link)
    #             self.log('the new url number is  %s' % self.not_scrapied_numer)
    #             yield Request('http://www.xiachufang.com%s' % link,
    #                           callback=self.parse_recipe)
    #         else:
    #             self.scrapied_numer += 1
    #             self.log('the total num crawled this time is  %s' % self.scrapied_numer)
    #             # self.log('this recipe has been scrapied, link is %s' % link)
    #             continue
    #
    #     # 横向爬取
    #     try:
    #         next_page = response.xpath('//a[@class="next"]//@href').extract()[0]
    #         yield Request(urljoin(response.url, next_page), callback=self.parse_category)
    #     except IndexError:
    #         return None
    
    # ------------------------------------------------------------------------------------------------------------------
    
    def parse_recipe(self, response):
        """ 解析菜谱详情并生成item
        @url http://www.xiachufang.com/recipe/1086136/
        @returns items 3
        @scrapes name cook cover_img rate_score
        @scrapes url project spider server date
        @scrapes name val recipe
        @scrapes name image_url step_order recipe
        """
        
        item = RecipeItem()
        
        item['image_urls'] = []
        # if response.status != 200:
        #     return None
        try:
            recipe_name = response.xpath('//h1[@itemprop="name"]/text()').extract()[0].strip()
        except IndexError:
            return
        
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
                item['image_urls'].append(s.xpath('img/@src').extract()[0] if s.xpath('img/@src').extract()[0] else \
                                              response.xpath('//img[@class="recipe-menu-cover"]/@src').extract()[i - 1])
            except IndexError:
                dict_steps['image_url'] = '暂无'
            list_steps.append(dict_steps)
        
        # ----------- parse the recipe -----------
        
        item['url'] = response.url
        recipe_category = response.xpath('//div[@class="recipe-cats"]/a/text()').extract()
        
        try:
            item['category'] = recipe_category
        except IndexError:
            item['category'] = '全部'
        try:
            item['fid'] = response.url.split('/')[-2]
        except IndexError:
            item['fid'] = '暂无'
        
        try:
            item['stars'] = response.xpath('//span[@class="number"]/text()').extract()[0]
        except IndexError:
            item['stars'] = 0
        
        try:
            item['cover_img'] = response.xpath('//div/div/img/@src').extract()[0]
            item['image_urls'].append((response.xpath('//div/div/img/@src').extract()[0]))
        except IndexError:
            item['cover_img'] = '暂无'
        try:
            item['cook'] = response.xpath('//span[@itemprop="name"]/text()').extract()[0]
        except IndexError:
            item['cook'] = '暂无'
        try:
            item['rate_score'] = response.xpath('//span[@itemprop="ratingValue"]/text()').extract()[0]
        except IndexError:
            item['rate_score'] = '5'
        try:
            item['name'] = response.xpath('//h1[@itemprop="name"]/text()').extract()[0].strip()
        except IndexError:
            item['name'] = '暂无'
        # try:
        #     item['brief'] = [x.strip() for x in response.xpath('//div[@itemprop="description"]/text()').extract()]
        # except IndexError:
        #     item['brief'] = '暂无'
        
        item['recipe_ingredients'] = list_ingre
        item['steps'] = list_steps
        # item['notice'] = [x.strip() for x in response.xpath('//div[@class="tip"]/text()').extract()]
        
        try:
            author_url = response.xpath('//div[@class="author"]/a/@href').extract()[0]
            yield Request(url='http://www.xiachufang.com' + author_url, meta={'item': item},
                          callback=self.parse_author)
        except IndexError:
            return
        
        recipe_menu_link_list = response.xpath('//a[contains(@class,"recipe-menu")]/@href').extract()
        
        if recipe_menu_link_list:
            for url in recipe_menu_link_list:
                yield Request('http://www.xiachufang.com' + url, callback=self.parse_recipe_list)
    
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
    
    def parse_recipe_list(self, response):
        item = RecepeListItem()
        item['fid'] = response.url.split('/')[-2]
        item['recipe_fids'] = response.xpath('//a').re('/recipe/\d+/')
        item['name'] = response.xpath('//h1/text()').extract()[0]
        item['created_member'] = response.xpath('//a[@class="avatar-link"]//@alt').extract()[0]
        item['recipes'] = response.xpath('//p[@class="name"]//a/text()').extract()
        item['fav_by'] = '暂无'
        yield item
