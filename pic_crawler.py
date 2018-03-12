#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' cdn_pic爬虫 '''

import os
import sys
import oss2
import time
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


def make_dir(path):
    '''
    make dir for pics
    '''
    if os.path.exists(path):
        pass
    else:
        os.mkdir(path)


def got_img(img_url):
    '''
    get the image body and type
    '''
    img_res = requests.get(img_url)
    try:
        img_data = Image.open(BytesIO(img_res.content))
        img_type = img_data.format.lower()
        return (img_data, img_type)
    except OSError:
        r.sadd('OSError_urls', img_url)
        return 0


def process_img(info, id, fid, dir, nameformat, order=None):
    ''' 保存图片并调用异步上传任务 '''
    if info:
        data = info[0]
        _type = info[1]
        cname_elements = (id, fid, order, _type) \
            if order else (id, fid, _type)
        imgname = nameformat % (cname_elements)
        filepath = dir + imgname
        data.save(filepath)
        upload_to_oss.delay(filepath)
        print(imgname)
    else:
        pass


def cdn_crawler():
    '''
    爬取图片保存到本地，再异步上传到OSS
    :return:
    '''
    dir_path = './OSS_PICS/'
    make_dir(dir_path)
    
    recipes = Recipe.objects.all()
    x = int(input('enter the start id: '))
    
    for recipe in recipes[x:]:
        cover_img_url = recipe.cover_img
        cover_info = got_img(cover_img_url)
        nameformat = 'i%sf%scover.%s'
        process_img(cover_info, recipe.id, recipe.fid, dir_path, nameformat)
        
        steps = recipe.recipestep_set.all()
        for order, step in enumerate(steps, 1):
            step_img = step.image_url
            if step_img != '暂无':
                step_info = got_img(step_img)
                nameformat = 'i%sf%ss%s.%s'
                process_img(step_info, recipe.id, recipe.fid, dir_path, nameformat, order)
            else:
                continue
        r.set('ossid', recipe.id)
    return None


if __name__ == '__main__':
    cdn_crawler()
