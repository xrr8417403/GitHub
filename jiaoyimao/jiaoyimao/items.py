# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy.loader.processors import MapCompose

def add_name(value):
    return value + "item_loader test!"

class JiaoyimaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #游戏名称
    #name = scrapy.Field(input_processor=MapCompose(add_name))
    name = scrapy.Field()
    #游戏商品总数
    total = scrapy.Field()
    #游戏商品类别
    category = scrapy.Field()
    #游戏商品数量
    count = scrapy.Field()
    #是否热门游戏
    ishot = scrapy.Field()
