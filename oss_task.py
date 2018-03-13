#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' 异步上传图片 '''

import os
import sys
import oss2
import time

from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@localhost//')

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


def percentage(consumed_bytes, total_bytes):
    """进度条回调函数，计算当前完成的百分比
    :param consumed_bytes: 已经上传/下载的数据量
    :param total_bytes: 总数据量
    """
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        print('\r{0:3}%  uploaded'.format(rate))
        sys.stdout.flush()


@app.task
def upload_to_oss(name):
    time.sleep(2)
    with open(name, 'rb') as data:
        bucket.put_object(name[11:], data, progress_callback=percentage)
    print('pic %s uploaded' % name[11:])
