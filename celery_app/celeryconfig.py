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
    # 'celery_app.ip_task',
    # 'celery_app.hello'
    # 'spider_task',
    # 'sql_task',
    # 'ip_task'
)

# schedules
CELERYBEAT_SCHEDULE = {
    # '获取免费ip': {
    #     'task': 'celery_app.ip_task.get_free_ip',
    #     'schedule': timedelta(seconds=10),  # 每 30 秒执行一次
    #     'args': None  # 任务函数参数
    # },
    # 'hello task': {
    #     'task': 'celery_app.hello.hello',
    #     'schedule': timedelta(seconds=10),  # 每 30 秒执行一次
    #     'schedule': crontab(hour=1, minute=22)
    # 'args': None  # 任务函数参数
    # },
    '定时启动 sql-worker': {
        'task': 'celery_app.sql_task.save_2_mysql',
        'schedule': crontab(hour=20, minute=10),  # 每晚 8 点 10 分执行一次
        'args': None  # 任务函数参数
    },
    '定时启动spider': {
        'task': 'celery_app.spider_task.start_spider',
        'schedule': crontab(),
    },
    # 'multiply-at-some-time': {
    #     'task': 'celery_app.hello.hello',
    #     'schedule': crontab(),  # 每天早上 9 点 50 分执行一次
    # }
}
