#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import json

# sys.path.insert(0, '/home/www/food_master/')

proj_path = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, proj_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'food_web.settings'
import django

django.setup()

from celery_app import r, app
from front.models import Member, Recipe, RecipeStep, Ingredient, RecipeIngredient, RecipeCategory, MemberRecipeList


@app.task
def save_list_2_mysql(v):
    if not v:
        print('消息丢失.')
        return None
    print('------start to save recip_list to MySQL--------')
    dict_list = json.loads(v)
    created_member = dict_list.get('created_member', 'anonymous')
    created_member_obj, status = Member.objects.get_or_create(name=created_member)
    list_obj, status = MemberRecipeList.objects.get_or_create(fid=dict_list.get('fid'),
                                                              name=dict_list.get('name'),
                                                              created_member=created_member_obj
                                                              )
    recipe_list = dict_list['recipes']
    recipe_fids = dict_list['recipe_fids']
    for rec, fid in zip(recipe_list, recipe_fids):
        recipe_obj = Recipe.objects.filter(name=rec, fid=fid)
        if recipe_obj:
            list_obj.recipes.add(recipe_obj[0])
        else:
            pass


@app.task
def save_recipe_2_mysql(v):
    if not v:
        print('消息丢失.')
        return None
    print('------start to save recipe to MySQL--------')
    dict_recipe = json.loads(v)
    cook_info = dict_recipe['cook']
    print('this url is -----%s' % dict_recipe['url'])
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
                                                  notice=dict_recipe.get('notice'),
                                                  cook=cook_obj)
    recipe.save()
    recipe.fav_by.add(cook_obj)
    
    for name in dict_recipe['category']:
        category, status = RecipeCategory.objects.get_or_create(name=name)
        recipe.category.add(category)
    
    for i in dict_recipe['steps']:
        RecipeStep.objects.get_or_create(step_order=i.get('step_order'),
                                         step_detail=i.get('step_detail'),
                                         image_url=i.get('image_url'),
                                         recipe=recipe)
    
    for i in dict_recipe['recipe_ingredients']:
        Ingredient.objects.get_or_create(name=i.get('ingredient'))
    
    for i in dict_recipe['recipe_ingredients']:
        RecipeIngredient.objects.get_or_create(
            recipe=Recipe.objects.filter(fid=dict_recipe.get('fid'), name=dict_recipe.get('name'),
                                         rate_score=dict_recipe.get('rate_score'))[0],
            ingredient=Ingredient.objects.filter(name=i['ingredient'])[0],
            usage=i.get('usage'))
    r.sadd('visited_urlset', dict_recipe['url'])
