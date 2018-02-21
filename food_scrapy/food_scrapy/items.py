# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


class FoodScrapyItem(scrapy.Item):
    '''
    define the fields for your item here like:
    name = scrapy.Field()
    '''
    
    # prime fields
    name = Field()
    cook = Field()
    brief = Field()
    steps = Field()
    images = Field()
    cover_img = Field()
    rate_score = Field()
    ingredients = Field()
    
    # other fields
    tag = Field()
    notice = Field()
    category = Field()
    
    # housekeeping fields
    url = Field()
    project = Field()
    spider = Field()
    server = Field()
    date = Field()


class IngredientItem(scrapy.Item):
    ingredient = Field()
    usage = Field()
    recipe = Field()


class RecipeStepItem(scrapy.Item):
    name = Field()
    step_order = Field()
    step_detail = Field()
    image_url = Field()
    recipe = Field()
