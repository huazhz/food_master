#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' sitemap生成脚本 '''
import os
import sys
import time
import requests
import imghdr
from PIL import Image
from io import BytesIO

# sys.path.insert(0, '/Users/macbook/个人项目/food_master')

proj_path = os.path.dirname(__file__)
sys.path.insert(0, proj_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'food_web.settings'
import django

django.setup()

from front.models import Recipe

recipes = Recipe.objects.all()

for recipe in recipes[95:]:
    
    cover_pic = recipe.cover_img
    res1 = requests.get(cover_pic)
    cover_pic = Image.open(BytesIO(res1.content))
    if not os.path.exists('./OSS_PICS'):
        os.mkdir('./OSS_PICS')
    cover_pic.save('./OSS_PICS/i%sf%scover.%s' % (recipe.id, recipe.fid, cover_pic.format.lower()))
    
    for order, step in enumerate(recipe.recipestep_set.all(), 1):
        step_img = step.image_url
        if step_img == '暂无':
            continue
        else:
            print('----- step image %s -----' % step.image_url)
            res = requests.get(step.image_url)
            step_pic = Image.open(BytesIO(res.content))
            print(step_pic.format)
            step_pic.save('./OSS_PICS/i%sf%ss%s.%s' % (recipe.id, recipe.fid, order, step_pic.format.lower()))
            time.sleep(0.2)
