import scrapy
import hashlib
import pymysql
from IR.items import IRItem
#该爬虫用于在sitesmap的基础上结合博客的推荐页面进行页面爬取
class ExampleSpider(scrapy.Spider):
    name = 'csdn'
    allowed_domains = ['csdn.net']
    start_urls = ["http://www.csdn.net"]

    def __init__(self, name=name):
        super().__init__(name=name)
        self.url_hashpool = set()
        #以sitesmap为初始网站集爬取csdn的网站
        with open("G:\code\IR\sitemap.txt",'r') as f:
            sites = f.readlines()
        self.destination_list = set(sites)
        self.id = 1
        self.state = {}
        try:
            #init hashpool
            self.db = pymysql.connect(host='localhost',user="root",password='12345678',database='lol',port=3306,charset='utf8')
            self.cursor = self.db.cursor()
            sql = "SELECT url_md5 FROM url_db WHERE title is not NULL"
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            self.url_hashpool.union(set(res))
            print("url_hashpool init success")
            #init id num
            sql = "SELECT id from url_db order by id DESC"
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            self.id = res[0][0]+1
            self.db.close()
            print("id init success:start at",self.id)
        except:
            print("url_hashpool init failed-database connect error")

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
        if response.url=="https://www.csdn.net":
            pass
        #对于csdn的blog，即保存页面信息及html，也获取链接
        elif(response.url.startswith("https://blog.csdn.net/") and response.url.find("details")!=-1):
            self.url_hashpool.add(md5)
            #构造item
            item = IRItem()
            item["keywords"] = response.xpath('/html/head//meta[@name="keywords"]/@content').extract()[0]
            item["description"] = response.xpath('/html/head//meta[@name="description"]/@content').extract()[0]
            item["title"] = response.xpath('/html/head/title/text()').extract()[0]
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
                    if (hashlib.md5(href.encode("utf8")).hexdigest()) not in self.url_hashpool:
                        self.destination_list.add(href)
        #对于csdn的搜索页，只获取其中的博客链接
        elif(response.url.startswith("https://so.csdn.net/so/search/")):
            all_href = response.xpath('//@href').extract()
            for href in all_href:
                if (href.startswith("https://blog.csdn.net/")):
                    href = self.robots_obey(href)
                    if (hashlib.md5(href.encode("utf8")).hexdigest()) not in self.url_hashpool:
                        self.destination_list.add(href)
        #等待队列为空时停止
        if(len(self.destination_list)==0):
            print("the waiting queue is empty")
            return
        #从等待队列获取下一个网址
        self.yield_next_url(2)
        for _ in range(2):
            next_url = self.destination_list.pop()
            if(next_url.startswith("https://blog.csdn.net/")):
                yield scrapy.Request(next_url,dont_filter=True)
            else:    
                keyword = next_url.split("/")[-1]
                next_url = "https://so.csdn.net/so/search/s.do?q="+keyword
                yield scrapy.Request(next_url,dont_filter=True)  

    def robots_obey(self,url):
        if(url.find("?")!=-1):
            return url.split("?")[0]
        else:
            return url

    def yield_next_url(self,num=2):
        for _ in range(num):
            next_url = self.destination_list.pop()
            if(next_url.startswith("https://blog.csdn.net/")):
                yield scrapy.Request(next_url,dont_filter=True)
            else:    
                keyword = next_url.split("/")[-1]
                next_url = "https://so.csdn.net/so/search/s.do?q="+keyword
                yield scrapy.Request(next_url,dont_filter=True)   
  