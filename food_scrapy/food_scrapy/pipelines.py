# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from scrapy.exceptions import DropItem
from .items import FoodScrapyItem, IngredientItem, RecipeStepItem
from front.models import RecipeStep, RecipeIngredient, Recipe


class FoodScrapyPipeline(object):
    
    def process_item(self, item, spider):
        ''' 分item存储数据 '''
        
        if isinstance(item, FoodScrapyItem):
            if item['name']:
                recipe = Recipe()
                recipe.name = item['name']
                recipe.cook = item['cook']
                recipe.brief = item['brief']
                recipe.rate_score = item['rate_score']
                recipe.cover_img = item['cover_img']
                # ...
                
                recipe.save()
                return item
            else:
                raise DropItem("this recipe is not available %s" % item)
        if isinstance(item, IngredientItem):
            if item['name']:
                ingredient = RecipeIngredient()
                # ingredient.recipe = to be done
                
                ingredient.save()
                return item
            else:
                raise DropItem('there is no nutrition')
        
        if isinstance(item, RecipeStepItem):
            if item['name']:
                self.recipestep = RecipeStep()
                
                return item
            else:
                raise DropItem('there is no steps')
        
        else:
            raise DropItem('the item is not what we want.')
