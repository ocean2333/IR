# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

class IrPipeline:

    def open_spider(self,spider):
        try:
            self.db = pymysql.connect(host='localhost',user="root",password='12345678',database='lol',port=3306,charset='utf8')
            self.cursor = self.db.cursor()
            print("mysql connect success")
        except:
            print("mysql connect error")

    def process_item(self, item, spider):
        if(item["id"]%100==0):
            print("start due with item",item["id"])
        sql = "INSERT IGNORE INTO test \
        (id,keywords, url, url_md5, pr, content, description,watch,create_date,favourite,title) \
         VALUES (%s,'%s','%s','%s',%s,'%s','%s',%s,'%s',%s,'%s')" % \
        (item["id"],item["keywords"],item["url"],item["url_md5"],item["pr"],item["content"],item["description"],item["watch"],item["date"],item["favourite"],item["title"])
        
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
            #print("insert data success")
        except:
            # 如果发生错误则回滚
            self.db.rollback() 
            print(sql)
            print("insert data error")

    def close_spoder(self,spider):
        self.db.close()



    