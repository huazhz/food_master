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


def get_img_body_and_type(img_url):
    '''
    获取图片的二进制数据和图片的类型
    返回一个包含上面信息的元组
    '''
    img_res = requests.get(img_url)
    try:
        img_data = Image.open(BytesIO(img_res.content))
        img_type = img_data.format.lower()
        return (img_data, img_type)
    except OSError:
        r.sadd('OSError_urls', img_url)
        return 0


def save_and_upload(info, id, fid, _dir, nameformat, order=None):
    ''' 保存图片并调用异步上传任务 '''
    if info:
        data = info[0]
        _type = info[1]
        name_elements = (id, fid, order, _type) \
            if order else (id, fid, _type)
        imgname = nameformat % name_elements
        filepath = _dir + imgname
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
        cover_img_info = get_img_body_and_type(cover_img_url)
        nameformat = 'i%sf%scover.%s'
        save_and_upload(cover_img_info, recipe.id, recipe.fid, dir_path, nameformat)
        
        steps = recipe.recipestep_set.all()
        for order, step in enumerate(steps, 1):
            step_img_url = step.image_url
            if step_img_url != '暂无':
                step_img_info = get_img_body_and_type(step_img_url)
                nameformat = 'i%sf%ss%s.%s'
                save_and_upload(step_img_info, recipe.id, recipe.fid, dir_path, nameformat, order)
            else:
                continue
        r.set('ossid', recipe.id)
    return None


if __name__ == '__main__':
    cdn_crawler()
