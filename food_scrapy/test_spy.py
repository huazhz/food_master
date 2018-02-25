#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests

proxies = {
    "http": "http://49.86.200.205:8118",
}
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'}
r = requests.get('http://www.xiachufang.com/recipe/101875766/', headers=headers, proxies=proxies)

print(r.status_code)
print(r.text)