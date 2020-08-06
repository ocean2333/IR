#just a test for whoosh
from whoosh.fields import *
from jieba.analyse import ChineseAnalyzer
#建立索引模式
analyzer = ChineseAnalyzer()
schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True,analyzer=analyzer))

import os.path
from whoosh.index import create_in
from whoosh.index import open_dir
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
for i in range(10):
    path = row[i][2]
    title = row[i][10]
    content = row[i][5]
    writer.add_document(path=path,title=title,content=content)
writer.commit()

from whoosh.qparser import QueryParser
from whoosh.query import And, Or, Term
ix = open_dir("index")
with ix.searcher() as searcher:
    query = And([Term('content',u'框架'), Term('content', u'服务')])    # 解析查询字符串后，生成一个`query`对象。
    res = searcher.search(query)
    print(res[0])
