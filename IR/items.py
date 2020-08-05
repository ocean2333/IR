# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ExampleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class IRItem(scrapy.Item): #创建一个类，继承scrapy.item类，就是继承人家写好的容器
    id = scrapy.Field() 
    keywords = scrapy.Field()
    url = scrapy.Field()
    url_md5 = scrapy.Field()
    pr = scrapy.Field()
    content = scrapy.Field()
    description = scrapy.Field()
    watch = scrapy.Field()
    favourite = scrapy.Field()
    date = scrapy.Field()
    title = scrapy.Field()
    
