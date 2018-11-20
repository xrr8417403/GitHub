import scrapy
from jiaoyimao.items import JiaoyimaoItem

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

        #for info in response.xpath('/html/body/div[4]/div[2]/div[2]/div[1]/div[1]/span/a'):
        #    yield response.follow(info,callback=self.parse)

        # yield { "name":response.css('div.mod-con.sel-content div h1::text').extract_first(),
        #        "count":response.css('span.em::text').extract_first()
        #}

        #for game_info in response.xpath()
            #yield {"name":[info.xpath('a/text()').extract()[0].strip(),info.xpath('a/@href').extract()[0].strip()]}
        #返回交易猫热门游戏的名称、链接
        #for game in response.xpath('//*[@id="scrollMain"]/div[1]/ul/li'):
        #    yield {
        #        'name':game.xpath('div[2]/a/h2/text()').extract(),
        #        'url':game.xpath('div[2]/a/@href').extract()
        #    }

    def parse_item(self,response):
        #从游戏详情页获取游戏名称
        name = response.xpath('//div[@class="breadcrumb"]/a[3]/text()').extract()
        #获取游戏总商品数
        total = int(response.xpath('//div[@class="more"]/span/text()').extract_first())
        if total > 0:
            for href in response.xpath('//div[@class="row row-sort"]/div[@class="con"]/span[@class="name"]'):
                category_url = href.xpath('a/@href').extract_first()
                category = href.xpath('a/text()').extract_first()
                print(category_url)
                yield scrapy.Request(category_url,callback=self.get_category,meta={"name":name,"total":total,"category":category})


    def get_category(self,response):
        #ITEM = JiaoyimaoItem()
        count = int(response.xpath('//div[@class="more"]/span/text()').extract_first())
        if count > 0:
            name = response.meta["name"]
            total = response.meta["total"]
            for sub_category_urls in response.xpath('//div[@class="row row-sort"]//span[@class="name"]'):
                sub_category_url = sub_category_urls.xpath('a/@href').extract_first()
                print(sub_category_url)
                sub_category = sub_category_urls.xpath('a/text()').extract_first()
                yield scrapy.Request(sub_category_url,callback=self.get_category_detal,meta={"name":name,"total":total,"sub_category":sub_category})
            #ITEM["category"] = response.meta["category"].strip()
            #ITEM["count"] = count
            #return ITEM

    def get_category_detal(self,response):
        ITEM = JiaoyimaoItem()
        count = int(response.xpath('//div[@class="more"]/span/text()').extract_first())
        if count > 0:
            ITEM["name"] = response.meta["name"]
            ITEM["total"] = response.meta["total"]
            ITEM["category"] = response.meta["sub_category"].strip()
            ITEM["count"] = count
            yield ITEM


'''
    def parse(self,response):
        for game in response.css("div#scrollMain>div>ul>li"):
            yield {
                'name':game.css('h2::text').extract(),
                'url':game.css('div.name>a::attr(href)').extract()
            }
'''