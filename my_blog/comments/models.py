from django.db import models


# 用户密码管理模型
class Users(models.Model):
    nickname = models.CharField(max_length=50, verbose_name='昵称', )
    email = models.EmailField(max_length=255, verbose_name='邮箱', )
    password = models.CharField(max_length=32, verbose_name="密码")
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    limit_choices = (
        (1, '未限制'),
        (2, '不能留言,留言不展示'),
        (2, '不能登录'),
    )
    limit = models.SmallIntegerField(choices=limit_choices,
                                     default=1,
                                     verbose_name="权限"
                                     )

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = "用户管理"
        verbose_name_plural = verbose_name


# 评论模型
class Comment(models.Model):
    text = models.TextField(verbose_name='留言内容', )
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', )
    is_delete = models.BooleanField(default=False, verbose_name='是否删除', )
    post = models.ForeignKey('blog.Post', verbose_name='评论区', )
    # 一对多
    users = models.ForeignKey(Users, verbose_name='评论')

    def __str__(self):
        return self.text[:20]

    class Meta:
        verbose_name = "评论区管理"
        verbose_name_plural = verbose_name
