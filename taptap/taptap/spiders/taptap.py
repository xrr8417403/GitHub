# _*_ coding: utf-8 _*_
import scrapy

class TaptapSpider(scrapy.Spider):

    name = 'taptap'
    #start_urls = ['https://www.taptap.com/top/download']
    headers = {
        'Host':"www.taptap.com",
        'Connection':"keep - alive",
        'Cache - Control':"max - age = 0",
        'Upgrade - Insecure - Requests': 1,
        'User - Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
        'Accept':"text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8",
        'Referer':"https: // www.taptap.com /",
        'Accept - Encoding':"gzip, deflate, br",
        'Accept - Language':"zh - CN, zh;q = 0.9",
        }

    def start_requests(self):
        yield scrapy.Request(url='https://www.taptap.com/top/download', callback=self.parse,headers=self.headers)

    def parse(self,response):
        print(response)