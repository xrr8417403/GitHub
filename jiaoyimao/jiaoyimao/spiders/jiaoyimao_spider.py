# _*_ coding: utf-8 _*_
import scrapy
from jiaoyimao.items import JiaoyimaoItem
from scrapy.loader import ItemLoader


class JiaoyimaoSpider(scrapy.Spider):

    name = 'jiaoyimao'

    start_urls = [
        'https://www.jiaoyimao.com/youxi/'
    ]

    def parse(self,response):
        #获取所有游戏商品的详情页
        for page_url in response.xpath('//ul[@class="game-list"]//div[@class="pic"]/a/@href'):
            yield response.follow(page_url,callback=self.parse_item)
            #yield scrapy.Request(url=page_url,callback=self.parse)



    def parse_item(self,response):
        #从游戏详情页获取游戏名称
        name = response.xpath('//div[@class="breadcrumb"]/a[3]/text()').extract()
        print("name:",name)
        #获取该游戏总商品数，若大于0则
        total = int(response.xpath('//div[@class="more"]/span/text()').extract_first())
        if total > 0:
            for href in response.xpath('//div[@class="row row-sort"]/div[@class="con"]/span[@class="name"]'):
                category_url = href.xpath('a/@href').extract_first()
                category = href.xpath('a/text()').extract_first()
                print("category:",category)
                yield scrapy.Request(category_url,callback=self.get_category,meta={"name":name,"total":total,"category":category})


    def get_category(self,response):
        #ITEM = JiaoyimaoItem()
        count = int(response.xpath('//div[@class="more"]/span/text()').extract_first())
        if count > 0:
            name = response.meta["name"]
            total = response.meta["total"]
            print("total:",total)
            for sub_category_urls in response.xpath('//div[@class="row row-sort"]//span[@class="name"]'):
                sub_category_url = sub_category_urls.xpath('a/@href').extract_first()
                print(sub_category_url)
                sub_category = sub_category_urls.xpath('a/text()').extract_first()
                yield scrapy.Request(sub_category_url,callback=self.get_category_detal,meta={"name":name,"total":total,"sub_category":sub_category})
            #ITEM["category"] = response.meta["category"].strip()
            #ITEM["count"] = count
            #return ITEM

    def get_category_detal(self,response):
        # item_loder 实现
        item_loder = ItemLoader(item=JiaoyimaoItem(),response=response)
        count = int(response.xpath('//div[@class="more"]/span/text()').extract_first())
        print("count:", count)
        if count > 0:
            item_loder.add_value('name',response.meta['name'])
            item_loder.add_value('total',response.meta['total'])
            item_loder.add_value('category',response.meta['sub_category'])
            item_loder.add_value('count',count)
            return item_loder.load_item()



'''
        # 直接使用ITEM实现
        ITEM = JiaoyimaoItem()
        count = int(response.xpath('//div[@class="more"]/span/text()').extract_first())
        if count > 0:
            ITEM["name"] = response.meta["name"]
            ITEM["total"] = response.meta["total"]
            ITEM["category"] = response.meta["sub_category"].strip()
            ITEM["count"] = count
            yield ITEM
'''

