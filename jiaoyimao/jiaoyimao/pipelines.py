# _*_ coding: utf-8 _*_


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
import pymysql

class JiaoyimaoPipeline(object):
    def process_item(self, item, spider):
        return item

class MySqlTwistedPipeline(object):

    def __init__(self,pool):
        self.dbpool = pool

    @classmethod
    def from_settings(cls,settings):
        params = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DB'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            port=settings['MYSQL_PORT'],
            charset=settings['MYSQL_CHARSET'],
            cursorclass=pymysql.cursors.DictCursor
        )
        dbpool = adbapi.ConnectionPool('pymysql',**params)

        return cls(dbpool)

    def process_item(self,item,spider):
        query = self.dbpool.runInteraction(self.insert_db,item)
        query.addErrback(self.handle_error)
        return item

    def handle_error(self,field):
        print("--------数据库写入失败：",field)

    def insert_db(self,cursor,item):
        insert_sql = " INSERT INTO GAME (name,category) VALUES(%s,%s)"
        cursor.execute(insert_sql,(item['name'],item['category']))
