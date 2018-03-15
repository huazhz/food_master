# !/usr/bin/env python
# -*- coding: utf-8 -*-

''' 统计首页访问时间 '''

import time
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class TimeItMiddleware(MiddlewareMixin):
    ''' count the total time '''
    
    def process_request(self, request):
        '''打印出所有参数'''
        # args = request.META
        # for k, v in args.items():
        #     print(k, v)
        # return None
    
    def process_view(self, request, func, *args, **kwargs):
        ''' 统计访问首页的时间 '''
        if request.path != reverse('index'):
            return None
        
        start = time.time()
        response = func(request)
        costed = time.time() - start
        print('{:.2f}s'.format(costed))
        return response
    
    def process_exception(self, request, exception):
        pass
    
    def process_template_response(self, request, response):
        return response
    
    def process_response(self, request, response):
        return response
