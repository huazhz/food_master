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
from oss_task import upload_to_oss

access_key_id = os.environ.get('access_key_id')
access_key_secret = os.environ.get('access_key_secret')
bucket_name = os.environ.get('bucket_name')
endpoint = os.environ.get('endpoint')  #

# test the environ
print(access_key_id)
print(access_key_secret)
print(bucket_name)
print(endpoint)

# 确认上面的参数都填写正确
for param in (access_key_id, access_key_secret, bucket_name, endpoint):
    assert '<' not in param, '请设置参数：' + param

bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)

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

recipes = Recipe.objects.all()

# 4563

for recipe in recipes[3683:]:
    cover_img_url = recipe.cover_img
    cover_res = requests.get(cover_img_url)
    cover_data = Image.open(BytesIO(cover_res.content))
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
            step_data = Image.open(BytesIO(step_res.content))
            sname_obj = (recipe.id, recipe.fid, order, step_data.format.lower())
            sname = 'i%sf%ss%s.%s' % sname_obj
            print(sname)
            sdata = step_res.content
            # bucket.put_object(sname, sdata, progress_callback=percentage)
            filepath2 = './OSS_PICS/i%sf%ss%s.%s' % sname_obj
            step_data.save(filepath2)
            upload_to_oss.delay(filepath2)
            # time.sleep(0.1)
