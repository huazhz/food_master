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
from celery_app import r, app

access_key_id = os.environ.get('access_key_id')
access_key_secret = os.environ.get('access_key_secret')
bucket_name = os.environ.get('bucket_name')
endpoint = os.environ.get('endpoint')  #

# 测试环境变量生效
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
from front.models import Recipe


def make_dir(path):
    '''
    为图片创建文件夹
    '''
    if os.path.exists(path):
        pass
    else:
        os.mkdir(path)


def img_exits(img):
    exist = bucket.object_exists(img)
    if exist:
        return True
    else:
        return False


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


def save_img(info, id, fid, _dir, nameformat, order=None):
    '''
    保存图片
    调用异步上传任务
    '''
    if info:
        data = info[0]
        _type = info[1]
        name_elements = (id, fid, order, _type) \
            if order else (id, fid, _type)
        img_name = nameformat % name_elements
        filepath = _dir + img_name
        data.save(filepath)
        assert os.path.exists(filepath) == True, 'file does not exists !!!'
        
        # upload_to_oss.delay(filepath)
        print(img_name)
    else:
        pass


def percentage(consumed_bytes, total_bytes):
    """进度条回调函数，计算当前完成的百分比
    :param consumed_bytes: 已经上传/下载的数据量
    :param total_bytes: 总数据量
    """
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        print('\r{0:3}%  uploaded'.format(rate))
        sys.stdout.flush()


def upload_to_oss(name):
    time.sleep(2)
    print('-' * 19)
    print(name)
    print(type(name))
    path = './oss_pics/' + name
    print('------path is %s-----' % path)
    with open(path, 'rb') as data:
        bucket.put_object(name, data, progress_callback=percentage)
    print('pic %s uploaded' % name)
    print('path %s uploaded' % path)
    if img_exits(name):
        os.remove(path)
    return None


@app.task
def cdn_crawler(id):
    '''
    爬取图片保存到本地
    异步上传到OSS
    '''
    img_list = []
    
    dir_path = './oss_pics/'
    make_dir(dir_path)
    
    recipe = Recipe.objects.get(id=id)
    cover_img_url = recipe.cover_img
    if cover_img_url != '暂无':
        cover_img_info = get_img_body_and_type(cover_img_url)
        if cover_img_info:
            nameformat = 'i%sf%scover.%s'
            cover_img_name = 'i%sf%scover.%s' % (recipe.id, recipe.fid, cover_img_info[1])
            recipe.cover_img = 'https://image.bestcaipu.com/' + cover_img_name
            recipe.save()
            img_list.append(cover_img_name)
            save_img(cover_img_info, recipe.id, recipe.fid, dir_path, nameformat)
    
    steps = recipe.recipestep_set.all()
    for order, step in enumerate(steps, 1):
        step_img_url = step.image_url
        if step_img_url != '暂无':
            step_img_info = get_img_body_and_type(step_img_url)
            if step_img_info:
                nameformat = 'i%sf%ss%s.%s'
                step_img_name = 'i%sf%ss%s.%s' % (recipe.id, recipe.fid, order, step_img_info[1])
                step.image_url = 'https://image.bestcaipu.com/' + step_img_name
                step.save()
                img_list.append(step_img_name)
                save_img(step_img_info, recipe.id, recipe.fid, dir_path, nameformat, order)
        else:
            continue
    
    for img in img_list:
        upload_to_oss(img)
    
    for img in img_list:
        if not img_exits(img):
            upload_to_oss(img)
