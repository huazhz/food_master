# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import redis
import datetime
from celery import Celery
from scrapy.exceptions import DropItem
from .items import FoodScrapyItem, IngredientItem, RecipeStepItem
from front.models import RecipeStep, RecipeIngredient, Recipe

broker = 'redis://127.0.0.1:6379'
backend = 'redis://127.0.0.1:6379/0'
app = Celery('tasks', broker=broker, backend=backend)


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
                insert_recipe2mysql.delay()
                return item
            else:
                raise DropItem("this recipe is not available %s" % item)
        if isinstance(item, IngredientItem):
            if item['name']:
                global r2
                v = json.dumps(item)
                r2.rpush('recipeingredient', v)
                insert_ingredient2mysql.delay()
                return item
            else:
                raise DropItem('there is no nutrition')
        
        if isinstance(item, RecipeStepItem):
            if item['name']:
                global r3
                v = json.dumps(item)
                r3.rpush('recipestep', v)
                insert_step2mysql.delay()
                return item
            else:
                raise DropItem('there is no steps')
        
        else:
            raise DropItem('the item is not what we want.')


@app.task
def insert_recipe2mysql():
    while r1:
        v = r1.lpop('recipe')
        item = json.loads(v)
        recipe = Recipe(fid=item['fid'],
                        name=item['name'],
                        cover_img=item['cover_img'],
                        rate_score=item['rate_score'],
                        brief=item['brief'],
                        cook=item['cook']
                        )
        recipe.save()


@app.task
def insert_ingredient2mysql():
    while r2:
        v = r2.lindex('recipeingredient', 0)
        item = json.loads(v)
        recipe_obj = Recipe.objects.filter(name=item['recipe'])[0]
        if not recipe_obj.exists():
            return None
        ingredient = RecipeIngredient(recipe=recipe_obj,
                                      ingredient=item['ingredient'],
                                      usage=item['usage']
                                      )
        ingredient.save()
        r2.lpop('recipeingredient')


@app.task
def insert_step2mysql():
    while r3:
        v = r3.lindex('recipestep', 0)
        item = json.loads(v)
        recipe_obj = Recipe.objects.filter(name=item['name'])
        if not recipe_obj.exists():
            return None
        steps = RecipeStep(name=item['name'],
                           step_order=item['step_order'],
                           step_detail=item['step_detail'],
                           image_url=item['image_url'],
                           recipe=recipe_obj,
                           add_time=datetime.datetime.now()
                           )
        steps.save()
        r3.lpop('recipestep')
