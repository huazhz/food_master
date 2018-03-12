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


def percentage(consumed_bytes, total_bytes):
    """进度条回调函数，计算当前完成的百分比
    :param consumed_bytes: 已经上传/下载的数据量
    :param total_bytes: 总数据量
    """
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        print('\r{0:3}%  uploaded'.format(rate))
        sys.stdout.flush()


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
        if cover_info:
            cname_elements = (recipe.id, recipe.fid, cover_info[1])
            cname = 'i%sf%scover.%s' % (cname_elements)
            filepath1 = dir_path + cname
            cover_info[0].save(filepath1)
            upload_to_oss.delay(filepath1)
            print(cname)
        else:
            continue
        
        steps = recipe.recipestep_set.all()
        
        for order, step in enumerate(steps, 1):
            step_img = step.image_url
            if step_img != '暂无':
                step_info = got_img(step_img)
                if step_info:
                    sname_obj = (recipe.id, recipe.fid, order, step_info[1])
                    sname = 'i%sf%ss%s.%s' % sname_obj
                    filepath2 = dir_path + sname
                    step_info[0].save(filepath2)
                    upload_to_oss.delay(filepath2)
                    print(sname)
            else:
                continue
        r.set('ossid', recipe.id)
    return None


if __name__ == '__main__':
    cdn_crawler()
