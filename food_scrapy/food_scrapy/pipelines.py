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
from front.models import RecipeStep, RecipeIngredient, Recipe, RecipeCategory

broker = 'redis://127.0.0.1:6379'
backend = 'redis://127.0.0.1:6379/0'
app = Celery('tasks', broker=broker, backend=backend)
pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
r = redis.Redis(connection_pool=pool)


class FoodScrapyPipeline(object):
    
    def process_item(self, item, spider):
        ''' 分item存储数据到redis列表，再通过celery异步写入MySQL '''
        
        if item['name']:
            v = json.dumps(dict(item))
            r.rpush('recipe', v)
            insert_2_mysql.delay()
            return item
        else:
            raise DropItem('the item is not available')


@app.task
def insert_2_mysql():
    # while r:
    v = r.lpop('recipe')
    dict_recipe = json.loads(v)
    recipe = Recipe(fid=dict_recipe['fid'],
                    name=dict_recipe['name'],
                    cover_img=dict_recipe['cover_img'],
                    rate_score=dict_recipe['rate_score'],
                    brief=dict_recipe['brief'],
                    # cook=dict_recipe['cook']
                    )
    recipe.save()
    for i in dict_recipe['ingredients']:
        RecipeStep.objects.create(step_order=i['step_order'],
                                  step_detail=i['step_detail'],
                                  image_url=i['image_url'],
                                  recipe=recipe)
    for i in dict_recipe['recipe_ingredients']:
        RecipeIngredient.objects.create(recipe=recipe,
                                        ingredient=i['ingredient'],
                                        usage=i['usage'])
