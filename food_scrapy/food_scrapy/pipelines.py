# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json
from celery_app.sql_task import save_recipe_2_mysql, save_list_2_mysql
from scrapy.exceptions import DropItem


class FoodScrapyPipeline(object):
    
    def process_item(self, item, spider):
        ''' 分item存储数据，再异步写入MySQL '''
        
        # if isinstance(item, RecipeItem):
        if item.get('cook'):
            v1 = json.dumps(dict(item))
            save_recipe_2_mysql.delay(v1)
            return item
        # elif isinstance(item, RecepeListItem):
        elif item.get('created_member'):
            v2 = json.dumps(dict(item))
            save_list_2_mysql.delay(v2)
        
        else:
            raise DropItem('the item is not available')
