from .models import blog
from haystack import indexes


class blogIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    keywords =  indexes.CharField(model_attr='keywords')
    title = indexes.CharField(model_attr='title')
    url = indexes.CharField(model_attr='url')
    date = indexes.CharField(model_attr="date")



    def get_model(self):
        return blog

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()