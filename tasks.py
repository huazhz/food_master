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
    
    cook_obj, status = Member.objects.get_or_create(name=cook_info.get('name'),
                                                    gender=cook_info.get('gender'),
                                                    email=cook_info.get('email'),
                                                    mobile=cook_info.get('email'),
                                                    password=cook_info.get('password'),
                                                    md5_password=cook_info.get('md5_password'),
                                                    is_fake=cook_info.get('is_fake'),
                                                    brief_intro=cook_info.get('brief_intro'),
                                                    join_ip=cook_info.get('join_ip'))
    
    recipe, status = Recipe.objects.get_or_create(fid=dict_recipe.get('fid'),
                                                  name=dict_recipe.get('name'),
                                                  cover_img=dict_recipe.get('cover_img'),
                                                  rate_score=dict_recipe.get('rate_score'),
                                                  brief=dict_recipe.get('brief'),
                                                  cook=cook_obj,
                                                  fav_by=cook_obj)
    recipe.save()
    
    for i in dict_recipe['steps']:
        RecipeStep.objects.get_or_create(step_order=i.get('step_order'),
                                         step_detail=i.get('step_detail'),
                                         image_url=i.get('image_url'),
                                         recipe=recipe)
        # recipe=Recipe.objects.filter(fid=dict_recipe.get('fid'),
        #                              name=dict_recipe.get('name')[0],
        #                              rate_score=dict_recipe.get('rate_score'))[0], )
    
    for i in dict_recipe['recipe_ingredients']:
        Ingredient.objects.get_or_create(name=i.get('ingredient'))
    
    for i in dict_recipe['recipe_ingredients']:
        RecipeIngredient.objects.get_or_create(
            recipe=Recipe.objects.filter(fid=dict_recipe.get('fid'), name=dict_recipe.get('name'),
                                         rate_score=dict_recipe.get('rate_score'))[0],
            ingredient=Ingredient.objects.filter(name=i['ingredient'])[0],
            usage=i.get('usage'))
    r.lpop('recipe')
