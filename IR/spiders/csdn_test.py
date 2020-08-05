import scrapy
import hashlib
import pymysql
import re
from IR.items import IRItem
#测试用爬虫
class ExampleSpider(scrapy.Spider):
    name = 'csdn_test'
    allowed_domains = ['csdn.net']
    start_urls = ["https://www.csdn.net/robots.txt"]

    def __init__(self, name=name):
        super().__init__(name=name)
        self.url_hashpool = set()
        #以sitesmap为初始网站集爬取csdn的网站
        self.destination_list = set(["http://www.csdn.net/tag/64bit"])
        self.id = 1
        self.robots_keywords = []

    def parse(self, response):
        print('start parse : ' + response.url)
        md5 = hashlib.md5(response.url.encode("utf8")).hexdigest()
        #利用url的MD5去重
        if(md5 in self.url_hashpool):
            next_url = self.destination_list.pop()
            keyword = next_url.split("/")[-1]
            next_url = "https://so.csdn.net/so/search/s.do?q="+keyword
            yield scrapy.Request(next_url,dont_filter=True)
            return
        #csdn首页
        if response.url=="https://www.csdn.net/robots.txt":
            pass
        #对于csdn的blog，即保存页面信息及html，也获取链接
        elif(response.url.startswith("https://blog.csdn.net/") and response.url.find("details")!=-1):
            self.url_hashpool.add(md5)
            #构造item
            item = IRItem()
            item["name"] = response.xpath('/html/head//meta[@name="keywords"]/@content').extract()[0]
            item["description"] = response.xpath('/html/head//meta[@name="description"]/@content').extract()[0]
            item["id"] = self.id
            self.id = self.id+1  
            item["url"] = response.url
            item["url_md5"] = md5
            item["pr"] = 0 
            item["content"] = response.xpath
            item["watch"] = int(response.xpath('/html/body//span[@class="read-count"]/text()').extract()[0])
            raw_fav = response.xpath('/html/body//span[@class="get-collection"]/text()').extract()[0].replace("\n","").replace(" ","")
            if(raw_fav==""):
                item["favourite"] = 0
            else:
                item["favourite"] = int(raw_fav)
            item["date"] = response.xpath('/html/body//div[@class="bar-content"]//span[@class="time"]/text()').extract()[0]
            #将item传入pipeline
            yield item         
            #获取链接 
            all_href = response.xpath('//@href').extract()
            for href in all_href:
                if (href.startswith("https://blog.csdn.net/")):
                    href = self.robots_obey(href)
                    self.destination_list.add(href)          
        #对于csdn的搜索页，只获取其中的博客链接
        elif(response.url.startswith("https://so.csdn.net/so/search/")):       
            all_href = response.xpath('//@href').extract()
            for href in all_href:
                if (href.startswith("https://blog.csdn.net/")):
                    href = self.robots_obey(href)
                    self.destination_list.add(href)         
        #等待队列为空时停止
        if(len(self.destination_list)==0):
            print("the waiting queue is empty")
            return
        #从等待队列获取下一个网址
        next_url = self.destination_list.pop()
        if(next_url.startswith("https://blog.csdn.net/")):
            yield scrapy.Request(next_url,dont_filter=True)
        elif(next_url.startswith("http://www.csdn.net/tag/")):    
            keyword = next_url.split("/")[-1]
            next_url = "https://so.csdn.net/so/search/s.do?q="+keyword
            yield scrapy.Request(next_url,dont_filter=True)
        else:
            pass
  
    def robots_obey(self,url):
        if(url.find("?")!=-1):
            return url.split("?")[0]
        else:
            return url