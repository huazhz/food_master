#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' 启动 webhook '''

# start_webkook.py
import os
from wsgiref.simple_server import make_server


def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    # os.system('git add .')
    # os.system('git commit -m "merge"')
    os.system('git pull origin master')
    print('git pull finish')
    return [b'Hello Webhook']


# 创建一个服务器，IP地址为空，端口是8000，处理函数是application:
httpd = make_server('', 443, application)
print('Serving HTTP on port 8000...')
# 开始监听HTTP请求:
httpd.serve_forever()
