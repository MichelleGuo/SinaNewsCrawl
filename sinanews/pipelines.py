# -*- coding: utf-8 -*-
import codecs
import json
from startWork import initialization


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class SinanewsPipeline(object):
    def __init__(self):
        filename,path = initialization()
        self.file = codecs.open(path + filename +'.json',mode='w',encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False)+'\n'
        # ensure_ascii=False很重要
        self.file.write(line)
        return item

    def close_spider(self,spider):
        self.file.close()
