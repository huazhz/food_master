#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' cdn_pic爬虫 '''

import os
import sys
import requests
from PIL import Image
from io import BytesIO
from celery_app import r
from oss_task import upload_to_oss

# setup Django environment
proj_path = os.path.dirname(__file__)
sys.path.insert(0, proj_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'food_web.settings'
import django

django.setup()

from front.models import Recipe

recipes = Recipe.objects.all()

for recipe in recipes[3703:]:
    cover_img_url = recipe.cover_img
    cover_res = requests.get(cover_img_url)
    cover_data = Image.open(BytesIO(cover_res.content))
    cname_obj = (recipe.id, recipe.fid, cover_data.format.lower())
    cname = 'i%sf%scover.%s' % (cname_obj)
    print(cname)
    r.set('ossid', recipe.id)
    cdata = cover_res.content
    if not os.path.exists('./OSS_PICS'):
        os.mkdir('./OSS_PICS')
    filepath = './OSS_PICS/i%sf%scover.%s' % cname_obj
    try:
        cover_data.save(filepath)
        upload_to_oss.delay(filepath)
    except IOError:
        r.sadd('IOError_urls', cover_img_url)
    
    for order, step in enumerate(recipe.recipestep_set.all(), 1):
        step_img = step.image_url
        if step_img == '暂无':
            continue
        else:
            step_res = requests.get(step.image_url)
            step_data = Image.open(BytesIO(step_res.content))
            sname_obj = (recipe.id, recipe.fid, order, step_data.format.lower())
            sname = 'i%sf%ss%s.%s' % sname_obj
            print(sname)
            sdata = step_res.content
            step_data.save('./OSS_PICS/i%sf%ss%s.%s' % sname_obj)
            filepath = './OSS_PICS/i%sf%ss%s.%s' % sname_obj
            try:
                cover_data.save(filepath)
                upload_to_oss.delay(filepath)
            except IOError:
                r.sadd('IOError_urls', step_img)
