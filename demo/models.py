from django.db import models

# Create your models here.
from django.db import models

class WeiboNote(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增ID')
    user_id = models.CharField(max_length=64, null=True, verbose_name='用户ID')
    nickname = models.CharField(max_length=64, null=True, verbose_name='用户昵称')
    avatar = models.CharField(max_length=255, null=True, verbose_name='用户头像地址')
    gender = models.CharField(max_length=12, null=True, verbose_name='用户性别')
    profile_url = models.CharField(max_length=255, null=True, verbose_name='用户主页地址')
    ip_location = models.CharField(max_length=32, default='发布微博的地理信息', verbose_name='发布微博的地理信息')
    add_ts = models.BigIntegerField(verbose_name='记录添加时间戳')
    last_modify_ts = models.BigIntegerField(verbose_name='记录最后修改时间戳')
    note_id = models.CharField(max_length=64, verbose_name='帖子ID')
    content = models.TextField(null=True, verbose_name='帖子正文内容')
    create_time = models.BigIntegerField(verbose_name='帖子发布时间戳')
    create_date_time = models.CharField(max_length=32, verbose_name='帖子发布日期时间')
    liked_count = models.CharField(max_length=16, null=True, verbose_name='帖子点赞数')
    comments_count = models.CharField(max_length=16, null=True, verbose_name='帖子评论数量')
    shared_count = models.CharField(max_length=16, null=True, verbose_name='帖子转发数量')
    note_url = models.CharField(max_length=512, null=True, verbose_name='帖子详情URL')

    def __str__(self):
        return self.note_id

    class Meta:
        db_table = 'weibo_note'  # 指定表名
        verbose_name = '微博帖子'  # 模型的人类可读名称
        verbose_name_plural = '微博帖子'  # 模型的人类可读复数名称


class WeiboNoteComment(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增ID')
    user_id = models.CharField(max_length=64, null=True, verbose_name='用户ID')
    nickname = models.CharField(max_length=64, null=True, verbose_name='用户昵称')
    avatar = models.CharField(max_length=255, null=True, verbose_name='用户头像地址')
    gender = models.CharField(max_length=12, null=True, verbose_name='用户性别')
    profile_url = models.CharField(max_length=255, null=True, verbose_name='用户主页地址')
    ip_location = models.CharField(max_length=32, default='发布微博的地理信息', verbose_name='发布微博的地理信息')
    add_ts = models.BigIntegerField(verbose_name='记录添加时间戳')
    last_modify_ts = models.BigIntegerField(verbose_name='记录最后修改时间戳')
    comment_id = models.CharField(max_length=64, verbose_name='评论ID')
    note_id = models.CharField(max_length=64, verbose_name='帖子ID')
    content = models.CharField(max_length=1000, null=True, verbose_name='评论内容')
    create_time = models.BigIntegerField(verbose_name='评论时间戳')
    create_date_time = models.CharField(max_length=32, verbose_name='评论日期时间')
    comment_like_count = models.CharField(max_length=16, verbose_name='评论点赞数量')
    sub_comment_count = models.CharField(max_length=16, verbose_name='评论回复数')

    def __str__(self):
        return self.comment_id


    class Meta:
        db_table = 'weibo_note_comment'  # 指定表名
        verbose_name = '微博帖子评论'  # 模型的人类可读名称
        verbose_name_plural = '微博帖子评论'  # 模型的人类可读复数名称


class KeyWordCrawl(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('doing', 'Doing'),
        ('done', 'Done'),
    )
    id = models.AutoField(primary_key=True, verbose_name='自增ID')
    keyword = models.CharField(max_length=100)
    count = models.IntegerField()
    isCrawlComment = models.BooleanField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.keyword

    class Meta:
        db_table = 'keyword_crawl'  # 指定表名
        verbose_name = '关键词爬虫'  # 模型的人类可读名称

class BlogCrawl(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('doing', 'Doing'),
        ('done', 'Done'),
    )
    id = models.AutoField(primary_key=True, verbose_name='自增ID')
    note_id = models.CharField( max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.note_id

    class Meta:
        db_table = 'note_id_crawl'  # 指定表名
        verbose_name = '指定博文爬虫'  # 模型的人类可读名称