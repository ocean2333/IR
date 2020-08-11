from .models import blog
from haystack import indexes


class blogIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    url = indexes.CharField(model_attr='url')

    def get_model(self):
        return blog

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        #确定在建立索引时有些记录被索引，这里我们简单地返回所有记录
        return self.get_model().objects.all()
'''
    def get_data_from_db(self):
        db = pymysql.connect(host='localhost',user="root",password='12345678',database='lol',port=3306,charset='utf8')
        cursor = db.cursor()
        sql = "select * from test"
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()  
            return rows
        except:
            print("error")
            return    

    def prepare_data(self):
        rows = self.get_data_from_db()
    
    def prepare(self,obj):
        self.prepared_data = super(DoubanMovieIndex, self).prepare(obj)
        self.prepared_data['_title_boost'] = 4.0

        return self.prepared_data
'''