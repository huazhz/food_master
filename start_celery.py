#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' 这个脚本用于启动 celery的worker和beat '''

import os

# 此处需要指定虚拟环境里的celery
celery_path = '.env/bin/celery'

os.system('nohup %s -A celery_app worker --loglevel=info -n worker1 &' % celery_path)
os.system('nohup %s -A celery_app worker --loglevel=info -n worker2 &' % celery_path)
os.system('nohup %s -A celery_app worker --loglevel=info -n worker3 &' % celery_path)

os.system('nohup %s -A celery_app beat --loglevel=info &' % celery_path)

# for test
# os.system('source venv/bin/activate && nohup celery -A celery_app worker --loglevel=info &')
# os.system('source venv/bin/activate && celery -A celery_app beat --loglevel=info')
