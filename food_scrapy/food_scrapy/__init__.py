import sys, os

# sys.path.append(r'/Users/macbook/个人项目/food_master/food_scrapy')

# sys.path.insert(0, '/home/www/food_master')
sys.path.insert(0, '/Users/macbook/个人项目/food_master')

os.environ['DJANGO_SETTINGS_MODULE'] = 'food_web.settings'
import django

django.setup()
