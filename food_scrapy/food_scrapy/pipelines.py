# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from scrapy.exceptions import DropItem
from .items import FoodScrapyItem, NutritionItem, RecipeStepItem


class FoodScrapyPipeline(object):
    
    def __init__(self):
        self.file1 = open('caipu.json', 'a')
        self.file2 = open('nutrition.json', 'a')
        self.file3 = open('step.json', 'a')
    
    def process_item(self, item, spider):
        ''' 分item存储数据 '''
        if isinstance(item, FoodScrapyItem):
            if item['name']:
                recipe = json.dumps(dict(item), ensure_ascii=False) + '\n'
                self.file1.write(recipe)
                return item
            else:
                raise DropItem("this recipe is not available %s" % item)
        if isinstance(item, NutritionItem):
            if item['name']:
                nutrition = json.dumps(dict(item), ensure_ascii=False) + '\n'
                self.file2.write(nutrition)
                return item
            else:
                raise DropItem('there is no nutrition')
        
        if isinstance(item, RecipeStepItem):
            if item['name']:
                step = json.dumps(dict(item), ensure_ascii=False) + '\n'
                self.file3.write(step)
                return item
            else:
                raise DropItem('there is no steps')
        
        else:
            raise DropItem('the item is not what we want.')
