import scrapy
import hashlib
import pymysql
from IR.items import IRItem

class ExampleSpider(scrapy.Spider):
    name = 'tieba'
    allowed_domains = ['tieba.baidu.com']
    start_urls = ['https://tieba.baidu.com']

    def __init__(self, name=name):
        super().__init__(name=name)
        self.url_hashpool = set()
        self.destination_list = set(['https://tieba.baidu.com'])
        self.id = 1

    def parse(self, response):
        print('start parse : ' + response.url)
        md5 = hashlib.md5(response.url.encode("utf8")).hexdigest()
        if(md5 in self.url_hashpool):
            next_url = self.destination_list.pop(0)
            yield scrapy.Request(next_url,dont_filter=True)
            return
        if response.url.startswith("https://tieba.baidu.com"):
            #构造item
            item = IRItem()
            item["name"] = response.xpath('/html/head//meta[@name="keywords"]/@content').extract()[0]
            item["description"] = response.xpath('/html/head//meta[@name="description"]/@content').extract()[0]
            item["id"] = self.id
            self.id = self.id+1  
            item["url"] = response.url
            item["url_md5"] = md5
            item["pr"] = 0
            #item["content"] = pymysql.escape_string(response.body.decode("utf8")) 
            item["content"] = response.xpath
            #提取链接
            all_href = response.xpath('//@href').extract()
            for href in all_href:
                if (href.startswith("/p/")):
                    self.destination_list.add('https://tieba.baidu.com'+href)
            #将item传入pipeline
            yield item
            self.url_hashpool.add(md5)
        if(len(self.destination_list)==0):
            print("the waiting queue is empty")
            return
        next_url = self.destination_list.pop()
        yield scrapy.Request(next_url,dont_filter=True)
  