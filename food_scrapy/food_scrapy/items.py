# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


class FoodScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    # prime fields
    name = Field()
    cook = Field()
    brief = Field()
    steps = Field()
    cover_img = Field()
    rate_score = Field()
    ingredients = Field()
    
    # other fields
    tag = Field()
    notice = Field()
    category = Field()
