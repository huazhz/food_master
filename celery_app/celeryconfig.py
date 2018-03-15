#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta
from celery.schedules import crontab

# Broker and Backend
# BROKER_URL = 'redis://127.0.0.1:6379'
BROKER_URL = 'pyamqp://guest@localhost//'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
# Timezone
CELERY_TIMEZONE = 'Asia/Shanghai'  # 坑，不生效，你大爷
# CELERY_TIMEZONE='UTC'

USE_TZ = True

# import
CELERY_IMPORTS = (
    'celery_app.spider_task',
    'celery_app.sql_task',
    'celery_app.ip_task',
    'celery_app.hello',
    'celery_app.img_crawler',
)

# schedules
CELERYBEAT_SCHEDULE = {
    '获取免费ip': {
        'task': 'celery_app.ip_task.get_free_ip',
        'schedule': crontab(minute='*/3'),  # 每3分钟执行一次，但仅限于0点到1点
    },
    'img_crawler': {
        'task': 'celery_app.img_crawler.cdn_crawler',
        'schedule': crontab(),  # 每3分钟执行一次，但仅限于0点到1点
    },
    '定时启动 sql-worker1': {
        'task': 'celery_app.sql_task.save_recipe_2_mysql',
        'schedule': crontab(minute=0, hour=4),  # 在凌晨12点开启
        'args': ('v',)
    },
    '定时启动 sql-worker2': {
        'task': 'celery_app.sql_task.save_list_2_mysql',
        'schedule': crontab(minute=0, hour=4),  # 在凌晨12点开启
        'args': ('v',),
    },
    '定时启动spider': {
        'task': 'celery_app.spider_task.start_spider',
        'schedule': crontab(minute='*/10', hour='0-2,5-9,12-23'),  # 爬虫除了中午12点和晚上6-8点，每10分钟执行一次，每次执行540秒
    },
    'hello test': {
        'task': 'celery_app.hello.hello',
        'schedule': crontab(),  # 没什么用，测试用的
    }
}
