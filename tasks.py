#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
from celery_app import r, app
from front.models import Member, Recipe, RecipeStep, Ingredient, RecipeIngredient


@app.task(name='tasks.save_2_mysql')
def save_2_mysql():
    v = r.lindex('recipe', 0)
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
    
    recipe = Recipe(fid=dict_recipe['fid'],
                    name=dict_recipe['name'],
                    cover_img=dict_recipe['cover_img'],
                    rate_score=dict_recipe['rate_score'],
                    brief=dict_recipe['brief'],
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
    r.lpop('recipe')
