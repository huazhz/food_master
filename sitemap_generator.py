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

## xml edition

# with open('sitemap.xml', 'a') as f:
#     for i in range(len(recipes)):
#         f.write('''\n    <url>
#         <loc>http://www.bestcaipu.com/recipe/%s/</loc>
#         <lastmod>2018-03-12T02:30:22+00:00</lastmod>
#         <priority>0.80</priority>
#     </url>''' % (i + 1))
#
#     f.write('\n</urlset>')


# txt edition
with open('sitemap.txt', 'a') as f:
    for i in range(len(recipes)):
        f.write('''https://www.bestcaipu.com/recipe/%s/\n''' % (i + 1))
    
    f.write('\n</urlset>')
