# _*_ coding: utf-8 _*_

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
from twisted.enterprise import adbapi


class JiaoyimaoPipeline(object):
    def process_item(self, item, spider):
        return item

class SqliteTwistedPipeline(object):

    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls):
        dbpool = adbapi.CoonectionPool('sqlite3','jiaoyimao.db')
        return cls(dbpool)

    def process_item(self,item,spider):
        query = self.dbpool.runInteraction(self.insert_db,item)
        query.addErrback(self.handle_error)
        return item

    def handle_error(self,field):
        print("--------数据库写入失败：",field)

    def insert_db(self,cursor,item):
        insert_sql = " INSERT INTO GAME (name,total,category,count) VALUES(%s,%s,%s,%s)"
        cursor.execute(insert_sql,(item['name'],item['total'],item['category'],item['cout']))

