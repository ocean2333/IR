#interface for query
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh.query import And, Or, Term
def query(keyword_list):
    pass



if __name__ == "__main__":
    ix = open_dir("index")
    with ix.searcher() as searcher:
        query = And([Term('content',u'框架'), Term('content', u'服务')])    # 解析查询字符串后，生成一个`query`对象。
        res = searcher.search(query)
        for r in res:
            print(r["title"])