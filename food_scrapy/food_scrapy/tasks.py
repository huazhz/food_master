#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
1. 检查先决条件
2. 定义子程序要解决的问题
3. 为子程序命名
4. 决定如何测试子程序
5. 在标准库中搜寻可用的功能
6. 考虑错误处理
7. 考虑效率问题
8. 研究算法和数据类型
9. 编写伪代码
    1. 首先简要地用一句话来写下该子程序的目的，
    2. 编写很高层次的伪代码
    3. 考虑数据
    4. 检查伪代码
10. 在伪代码中试验一些想法，留下最好的想法
'''
import json
from food_scrapy.celery_app import r, app
from front.models import Member, Recipe, RecipeStep, Ingredient, RecipeIngredient


@app.task(name='tasks.save_2_mysql')
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

# def get_free_ip(headers, url):
#     response = requests.get(url, headers=headers)
#     infos = json.loads(response.text)
#
#     s = []
#     for i in infos['msg']:
#         ip = i['ip']
#         port = i['port']
#         proxy = "http://%s:%s" % (ip, port)
#         if not s or proxy not in s:
#             s.append(proxy)
#             r.rpush('ip_list', proxy)
#         else:
#             s.append(proxy)
#             s.pop(0)
#             r.rpush('ip_list', proxy)
#     while r.llen('ip_list') > 5:
#         r.ltrim('ip_list', -5, -1)
#     return s
