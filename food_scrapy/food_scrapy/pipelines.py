# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from food_scrapy.celery_app import r
from food_scrapy.tasks import save_2_mysql
from scrapy.exceptions import DropItem
from front.models import Member, Recipe, RecipeStep, Ingredient, RecipeIngredient


class FoodScrapyPipeline(object):
    
    def process_item(self, item, spider):
        ''' 分item存储数据到redis列表，再通过celery异步写入MySQL '''
        
        if item['name']:
            v = json.dumps(dict(item))
            r.rpush('recipe', v)
            save_2_mysql.delay()
            return item
        else:
            raise DropItem('the item is not available')
