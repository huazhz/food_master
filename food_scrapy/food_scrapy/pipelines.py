# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from scrapy.exceptions import DropItem


class FoodScrapyPipeline(object):
    
    def __init__(self):
        self.file = open('caipu.json', 'a')
    
    def process_item(self, item, spider):
        if item['name']:
            recipe = json.dumps(dict(item)) + '\n'
            self.file.write(recipe)
            return item
        else:
            raise DropItem("this recipe is not available %s" % item)
