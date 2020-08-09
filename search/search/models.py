from django.db import models

class blog(models.Model):
    """post 文章页面"""
    id = models.AutoField(primary_key=True, max_length=20)
    name = models.CharField(max_length=200, help_text="Post文章的URL链接名称")
    #post_category = models.ForeignKey(PostCategory, blank=True, null=True, default=None, on_delete=models.SET_NULL)
    date = models.DateTimeField(default=timezone.now, help_text="创建日期")
    content = models.TextField(help_text="html格式的页面内容，仅在page类型才可用")
    title = models.CharField(max_length=200)

    # post_slug = models.CharField(max_length=200, help_text="URL链接名称")

    def __str__(self):
        return self.post_title