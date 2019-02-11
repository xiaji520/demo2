from django.conf.urls import url

from blog.views import IndexView, BlogView, AboutView, ContactView, DetailView, ArchivesView, CategoryView, TagView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='首页'),
    url(r'^detail/(?P<pk>[0-9]+)/$', DetailView.as_view(), name='详情'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', ArchivesView.as_view(), name='归档'),
    url(r'^category/(?P<pk>[0-9]+)/$', CategoryView.as_view(), name='分类'),
    url(r'^tag/(?P<pk>[0-9]+)/$', TagView.as_view(), name='标签'),
    url(r'^blog$', BlogView.as_view(), name='博客'),
    url(r'^about$', AboutView.as_view(), name='关于'),
    url(r'^contact$', ContactView.as_view(), name='联系'),

]
