# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from food_scrapy.config import r, app
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


@app.task(name='pipelines.save_2_mysql')
def save_2_mysql():
    v = r.lpop('recipe')
    dict_recipe = json.loads(v)
    cook_info = dict_recipe['cook']
    cook_obj, status = Member.objects.get_or_create(name=cook_info['name'],
                                                    gender=cook_info['gender'],
                                                    email=cook_info['email'],
                                                    mobile=cook_info['email'],
                                                    password=cook_info['password'],
                                                    md5_password=cook_info['md5_password'],
                                                    is_fake=cook_info['is_fake'],
                                                    brief_intro=cook_info['brief_intro'],
                                                    join_ip=cook_info['join_ip'])
    
    recipe = Recipe(fid=dict_recipe['fid'][0],
                    name=dict_recipe['name'][0],
                    cover_img=dict_recipe['cover_img'][0],
                    rate_score=dict_recipe['rate_score'][0],
                    brief=dict_recipe['brief'][0],
                    cook=cook_obj,
                    fav_by=cook_obj)
    recipe.save()
    
    for i in dict_recipe['steps']:
        RecipeStep.objects.get_or_create(step_order=i['step_order'],
                                         step_detail=i['step_detail'],
                                         image_url=i['image_url'],
                                         recipe=recipe)
    
    for i in dict_recipe['recipe_ingredients']:
        Ingredient.objects.get_or_create(name=i['ingredient'])
    
    for i in dict_recipe['recipe_ingredients']:
        RecipeIngredient.objects.get_or_create(recipe=recipe,
                                               ingredient=Ingredient.objects.filter(name=i['ingredient'])[0],
                                               usage=i['usage'])
