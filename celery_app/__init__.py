#!/usr/bin/env python
# -*- coding: utf-8 -*-


import redis
from celery import Celery

# from celery_app.celeryconfig import broker, backend

app = Celery('tasks')
app.config_from_object('celery_app.celeryconfig')

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
r = redis.Redis(connection_pool=pool)
