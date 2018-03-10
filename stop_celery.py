#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' this script is used to shutdown celery'''

import os

celery_path = '.env/bin/celery'
os.system('%s -A celery_app control shutdown' % celery_path)
