from django.conf.urls import url, include
from comments.views import RegisterView, LogintView, Post_commentView

urlpatterns = [
    url(r'^register$', RegisterView.as_view(), name='注册'),
    url(r'^login$', LogintView.as_view(), name='登录'),
    url(r'^comment/post/(?P<post_pk>[0-9]+)/$', Post_commentView.as_view(), name='文章评论'),
]
