# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class RecipeItem(scrapy.Item):
    fid = Field()
    name = Field()
    cover_img = Field()
    rate_score = Field()
    brief = Field()
    cook = Field()
    recipe_ingredients = Field()
    category = Field()
    fave_by = Field()
    tag = Field()
    steps = Field()
    url = Field()
    notice = Field()
    image_urls = Field()
    images = Field()


class RecepeListItem(scrapy.Item):
    fid = Field()
    name = Field()
    recipe_fids = Field()
    created_member = Field()
    recipes = Field()
    fav_by = Field()


class PatchItem(scrapy.Item):
    fid = Field()
    stars = Field()
    brief = Field()
