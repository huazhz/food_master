#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import json
from celery import Celery

from django.core.exceptions import ObjectDoesNotExist

proj_path = os.path.dirname(__file__)
sys.path.insert(0, proj_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'food_web.settings'

import django

django.setup()

from front.models import Recipe

app = Celery('tasks', broker='pyamqp://guest@localhost//')


@app.task(name='food_scrapy.spiders.xiachufangpatch.patch_xiachufang')
def patch_xiachufang(v):
    print('start to tools the spider')
    infos = json.loads(v)
    fid = infos.get('fid')
    print('the fid is %s' % fid)
    try:
        recipe_obj = Recipe.objects.get(fid=fid)
        print('get the object')
        recipe_obj.stars = infos.get('stars')
        
        recipe_obj.save()
        if recipe_obj.stars == infos.get('stars') and recipe_obj.stars != 0:
            print('succeed updated stars number')
    
    except ObjectDoesNotExist:
        pass
