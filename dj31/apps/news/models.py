from django.db import models

# Create your models here.
from dj31.utils.models import ModelBase
import pytz
'''
1 分类导航  name
2 轮播图 图片  优先级
3 热门新闻  关联news  优先级
4 图片  标题 重点 点击量 内容  时间 关联【作者 分类】

'''
from django.db import models

# from utils.models import ModelBase

#新闻标签
class Tag(ModelBase):
    """
    """
    name = models.CharField(max_length=64, verbose_name="标签名", help_text="标签名")

    class Meta:
        ordering = ['-update_time', '-id']
        db_table = "tb_tag"  # 指明数据库表名
        verbose_name = "新闻标签"  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称

    def __str__(self):
        return self.name

#新闻
class News(ModelBase):
    """
    """
    title = models.CharField(max_length=150, verbose_name="标题", help_text="标题")
    digest = models.CharField(max_length=200, verbose_name="摘要", help_text="摘要")
    content = models.TextField(verbose_name="内容", help_text="内容")
    clicks = models.IntegerField(default=0, verbose_name="点击量", help_text="点击量")
    image_url = models.URLField(default="", verbose_name="图片url", help_text="图片url")
    tag = models.ForeignKey('Tag', on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey('users.Users', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-update_time', '-id']
        db_table = "tb_news"  # 指明数据库表名
        verbose_name = "新闻"  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称

    def __str__(self):
        return self.title

    def in_clicks(self):
        self.clicks += 1
        self.save(update_fields=['clicks'])

#评论
class Comments(ModelBase):
    """
    """
    content = models.TextField(verbose_name="内容", help_text="内容")

    author = models.ForeignKey('users.Users', on_delete=models.SET_NULL, null=True)
    news = models.ForeignKey('News', on_delete=models.CASCADE)
    partent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        ordering = ['-update_time', '-id']
        db_table = "tb_comments"  # 指明数据库表名
        verbose_name = "评论"  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称



    def __str__(self):
        return '<评论{}>'.format(self.id)
    def to_dict(self):
        ss = pytz.country_timezones('cn')
        cn =pytz.timezone(ss[0])
        new_time=cn.normalize(self.update_time)

        comm_dict ={
            'news_id':self.news_id,
            'content_id':self.id,
            'content':self.content,
            'author':self.author.username,
            'update_time':new_time.strftime('%Y年%m月%d日 %H:%M'),
            'partent':self.partent.to_dict()if self.partent_id else None,


        }
        return comm_dict




#热门新闻
class HotNews(ModelBase):
    """
    """
    P_CHOICES = [
        (1, '第一级'),
        (2, '第二级'),
        (3, '第三级'),
    ]
    news = models.OneToOneField('News', on_delete=models.CASCADE)
    priority = models.IntegerField(verbose_name="优先级", help_text="优先级",choices=P_CHOICES)

    class Meta:
        ordering = ['-update_time', '-id']
        db_table = "tb_hotnews"  # 指明数据库表名
        verbose_name = "热门新闻"  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称

    def __str__(self):
        return '<热门新闻{}>'.format(self.id)

#轮播图
class Banner(ModelBase):
    """
    """
    image_url = models.URLField(verbose_name="轮播图url", help_text="轮播图url")
    B_CHOICES = [
        (1, '第一级'),
        (2, '第二级'),
        (3, '第三级'),
        (4, '第四级'),
        (5, '第五级'),
        (6, '第六级'),
    ]
    priority = models.IntegerField(verbose_name="优先级", help_text="优先级")
    news = models.OneToOneField('News', on_delete=models.CASCADE,choices=B_CHOICES,default=6)

    class Meta:
        ordering = ['priority', '-update_time', '-id']
        db_table = "tb_banner"  # 指明数据库表名
        verbose_name = "轮播图"  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称

    def __str__(self):
        return '<轮播图{}>'.format(self.id)
