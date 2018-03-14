#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' sitemap生成脚本 '''
import os
import sys
import json

# sys.path.insert(0, '/Users/macbook/个人项目/food_master')

proj_path = os.path.dirname(__file__)
sys.path.insert(0, proj_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'food_web.settings'
import django

django.setup()

from front.models import Recipe

recipes = Recipe.objects.all()

nameformat = 'https://image.bestcaipu.com/i%sf%scover.%s'
nameformat1 = 'https://image.bestcaipu.com/i%sf%ss%s.%s'

# nameformat % (rec.id, rec.fid, 'jpeg')

for rec in recipes:
    rec.cover_img = nameformat % (rec.id, rec.fid, 'jpeg')
    rec.save()
    print(rec.cover_img)
    
    steps = rec.recipestep_set.all()
    for order, step in enumerate(steps, 1):
        step.image_url = nameformat1 % (rec.id, rec.fid, order, 'jpeg')
        step.save()
        print(step.image_url)
        # print('--- step ---')
    print('-------- recipe -----------')

# print('https://image.bestcaipu.com/i%sf%ss%s.%s' % (1, 2, 3, 'jpeg'))
