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


def cdn_crawler():
    '''
    爬取图片保存到本地，再异步上传到OSS
    :return:
    '''
    recipes = Recipe.objects.all()
    x = int(input('enter the start id: '))
    for recipe in recipes[x:]:
        cover_img_url = recipe.cover_img
        cover_res = requests.get(cover_img_url)
        try:
            cover_data = Image.open(BytesIO(cover_res.content))
        except OSError:
            r.sadd('OSError_urls', recipe.cover_img)
            continue
        cname_obj = (recipe.id, recipe.fid, cover_data.format.lower())
        cname = 'i%sf%scover.%s' % (cname_obj)
        print(cname)
        cdata = cover_res.content
        # bucket.put_object(cname, cdata, progress_callback=percentage)
        # if not os.path.exists('./OSS_PICS'):
        #     os.mkdir('./OSS_PICS')
        filepath1 = './OSS_PICS/i%sf%scover.%s' % cname_obj
        cover_data.save(filepath1)
        upload_to_oss.delay(filepath1)
        
        for order, step in enumerate(recipe.recipestep_set.all(), 1):
            step_img = step.image_url
            if step_img == '暂无':
                continue
            else:
                step_res = requests.get(step.image_url)
                try:
                    step_data = Image.open(BytesIO(step_res.content))
                except OSError:
                    r.sadd('OSError_urls', step_img)
                    continue
                sname_obj = (recipe.id, recipe.fid, order, step_data.format.lower())
                sname = 'i%sf%ss%s.%s' % sname_obj
                print(sname)
                sdata = step_res.content
                # bucket.put_object(sname, sdata, progress_callback=percentage)
                filepath2 = './OSS_PICS/i%sf%ss%s.%s' % sname_obj
                step_data.save(filepath2)
                upload_to_oss.delay(filepath2)
                # time.sleep(0.1)
        r.set('ossid', recipe.id)
    return None


if __name__ == '__main__':
    cdn_crawler()
