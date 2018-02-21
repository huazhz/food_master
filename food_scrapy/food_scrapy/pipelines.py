# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import redis
import datetime
from scrapy.exceptions import DropItem
from .items import FoodScrapyItem, IngredientItem, RecipeStepItem
from front.models import RecipeStep, RecipeIngredient, Recipe

import time
from celery import Celery

broker = 'redis://127.0.0.1:6379'
backend = 'redis://127.0.0.1:6379/0'
app = Celery('my_task', broker=broker, backend=backend)


class FoodScrapyPipeline(object):
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
    r1 = redis.Redis(connection_pool=pool)
    r2 = redis.Redis(connection_pool=pool)
    r3 = redis.Redis(connection_pool=pool)
    
    def process_item(self, item, spider):
        ''' 分item存储数据到redis列表，再通过celery异步写入MySQL '''
        
        if isinstance(item, FoodScrapyItem):
            if item['name']:
                global r1
                v = json.dumps(item)
                r1.rpush('recipe', v)
                insert_recipe_2mysql.delay()
                return item
            else:
                raise DropItem("this recipe is not available %s" % item)
        if isinstance(item, IngredientItem):
            if item['name']:
                global r2
                v = json.dumps(item)
                r2.rpush('recipeingredient', v)
                insert_ingredient_2mysql.delay()
                return item
            else:
                raise DropItem('there is no nutrition')
        
        if isinstance(item, RecipeStepItem):
            if item['name']:
                global r3
                v = json.dumps(item)
                r3.rpush('recipestep', v)
                insert_step_2mysql.delay()
                return item
            else:
                raise DropItem('there is no steps')
        
        else:
            raise DropItem('the item is not what we want.')


@app.task
def insert_recipe_2mysql():
    while r1:
        v = r1.lpop('recipe')
        item = json.loads(v)
        recipe = Recipe(fid=item['fid'],
                        name=item['name'],
                        cover_img=item['cover_img'],
                        rate_score=item['rate_score'],
                        brief=item['brief'],
                        cook=item['cook'], )
        recipe.save()


@app.task
def insert_ingredient_2mysql():
    while r2:
        v = r2.lpop('recipeingredient')
        item = json.loads(v)
        recipe_obj = Recipe.objects.get(name=item['recipe'])
        ingredient = RecipeIngredient(recipe=recipe_obj,
                                      ingredient=item['ingredient'],
                                      usage=item['usage'], )
        ingredient.save()


@app.task
def insert_step_2mysql():
    while r3:
        v = r3.lpop('recipestep')
        item = json.loads(v)
        recipe_obj = Recipe.objects.get(name=item['name'])
        steps = RecipeStep(name=item['name'],
                           step_order=item['step_order'],
                           step_detail=item['step_detail'],
                           image_url=item['image_url'],
                           recipe=recipe_obj,
                           add_time=datetime.datetime.now(), )
        steps.save()
