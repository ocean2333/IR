from jieba.analyse import ChineseAnalyzer
from jieba import tokenize
quary = u"java服务器搭建"
esult = tokenize(quary,mode="search")
for tk in esult:
    print(tk[0])