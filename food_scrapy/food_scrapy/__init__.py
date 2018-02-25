import sys, os

# sys.path.append(r'/Users/macbook/个人项目/food_master/food_scrapy')

sys.path.insert(0, '/Users/macbook/个人项目/food_master')

os.environ['DJANGO_SETTINGS_MODULE'] = 'food_web.settings'
import django

django.setup()

import redis
from celery import Celery

broker = 'redis://127.0.0.1:6379'
backend = 'redis://127.0.0.1:6379/0'
app = Celery('tasks', broker=broker, backend=backend)
pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
r = redis.Redis(connection_pool=pool)
