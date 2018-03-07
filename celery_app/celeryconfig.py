#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta
from celery.schedules import crontab

# Broker and Backend
# BROKER_URL = 'redis://127.0.0.1:6379'
BROKER_URL = 'pyamqp://guest@localhost//'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
# Timezone
CELERY_TIMEZONE = 'Asia/Shanghai'  # 指定时区，不指定默认为 'UTC'
# CELERY_TIMEZONE='UTC'


# import
CELERY_IMPORTS = (
    'celery_app.spider_task',
    'celery_app.sql_task',
    'celery_app.ip_task',
    'celery_app.hello'
)

# schedules
CELERYBEAT_SCHEDULE = {
    '获取免费ip': {
        'task': 'celery_app.ip_task.get_free_ip',
        'schedule': crontab(minute='*/3'),  # 每3分钟执行一次，但仅限于0点到1点
    },
    '定时启动 sql-worker': {
        'task': 'celery_app.sql_task.save_2_mysql',
        'schedule': crontab(minute='*/10'),  # 每 10 分钟执行一次
        'args': ('v',),
    },
    '定时启动spider': {
        'task': 'celery_app.spider_task.start_spider',
        'schedule': crontab(minute='*/10'),  # 每10分钟执行一次，但仅限于0点到1点
    },
    'hello test': {
        'task': 'celery_app.hello.hello',
        'schedule': crontab(),  # 每天早上 9 点 50 分执行一次
    }
}
