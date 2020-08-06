#make everything in db indexed
from whoosh.fields import *
from jieba.analyse import ChineseAnalyzer
import os.path
from whoosh.index import create_in
from whoosh.index import open_dir

analyzer = ChineseAnalyzer()
schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True,analyzer=analyzer))

if not os.path.exists('index'):     #如果目录index不存在则创建
    os.mkdir('index') 
ix = create_in("index",schema)      #按照schema模式建立索引目录
ix = open_dir("index")              #打开该目录以便存储索引文件

import pymysql
db = pymysql.connect(host='localhost',user="root",password='12345678',database='lol',port=3306,charset='utf8')
cursor = db.cursor()
sql = "select * from test"
try:
    cursor.execute(sql)
    row = cursor.fetchall()  
except:
    print("error")

writer = ix.writer()
for i in range(len(row)):
    path = row[i][2]
    title = row[i][10]
    content = row[i][5]
    writer.add_document(path=path,title=title,content=content)
writer.commit()