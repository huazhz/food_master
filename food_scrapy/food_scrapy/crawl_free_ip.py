#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
从代理网站抓免费试用ip，每5分钟换一次
'''

headers = {'User-Agent': 'Mozilla/4.0 (compatible; IBrowse 3.0; AmigaOS4.0)'}
url = 'http://www.mogumiao.com/proxy/free/listFreeIp'

import json

import requests
from food_scrapy.config import r


def get_free_ip(headers, url):
    response = requests.get(url, headers=headers)
    infos = json.loads(response.text)
    
    s = []
    for i in infos['msg']:
        ip = i['ip']
        port = i['port']
        proxy = "http://%s:%s" % (ip, port)
        if not s or proxy not in s:
            s.append(proxy)
            r.rpush('ip_list', proxy)
        else:
            s.append(proxy)
            s.pop(0)
            r.rpush('ip_list', proxy)
    while r.llen('ip_list') > 5:
        r.ltrim('ip_list', -5, -1)
    return s


print(get_free_ip(headers, url))


def get_ips():
    ips = [i.decode('utf-8') for i in r.lrange('ip_list', -5, -1)]
    print(ips)
    return ips
