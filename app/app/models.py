from django.db import models
from datetime import timezone
class blog(models.Model):
    """post 文章页面"""
    id = models.IntegerField(primary_key=True, max_length=20)
    date = models.DateField(help_text="创建日期")
    content = models.TextField(help_text="html格式的页面内容，仅在page类型才可用")
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200, help_text="URL链接名称")

    def __str__(self):
        return self.post_title