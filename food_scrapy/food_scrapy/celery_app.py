#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis
from celery import Celery

broker = 'redis://127.0.0.1:6379'
backend = 'redis://127.0.0.1:6379/0'

app = Celery('mysqltask', broker=broker, backend=backend)

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
r = redis.Redis(connection_pool=pool)

if __name__ == '__main__':
    app.start()
