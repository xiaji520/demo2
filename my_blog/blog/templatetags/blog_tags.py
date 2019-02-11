from django import template
from django.db.models import Count

from ..models import Post, Category, Tag

register = template.Library()

# 最新文章模板标签
'''
导入 template 这个模块，然后实例化了一个 template.Library 类，
并将函数 get_recent_posts 装饰为 register.simple_tag
这样就可以在模板中使用语法 {% get_recent_posts %} 调用这个函数了
'''


@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.filter(is_delete=False).order_by('-created_time')[:num]


# 归档模板标签
@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')


# 分类模板标签
@register.simple_tag
def get_categories():
    # 别忘了在顶部引入 Category 类
    return Category.objects.all()


@register.simple_tag
def get_tags():
    # 记得在顶部引入 Tag model
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
