import markdown
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView

from blog.models import Post, Category, Tag
from comments.models import Comment
from db.base_view import VerifyLoginView


class IndexView(View):
    '''
    首页
    '''

    def get(self, request):
        # 渲染页面
        post_list = Post.objects.filter(is_delete=False).order_by('-created_time')

        # 分页
        paginator = Paginator(post_list, 5)  # 每页显示n条记录
        # 获取当前页码数据
        page = request.GET.get('page', 1)  # 当前页码?Page=1
        # 获取对应页码数据
        try:
            post_list = paginator.page(page)
        except PageNotAnInteger:
            # 页码不是整数 显示第一页
            post_list = paginator.page(1)
        except EmptyPage:
            # 页码为空 显示最后一页
            post_list = paginator.page(paginator.num_pages)

        context = {
            'post_list': post_list,
        }
        return render(request, 'blog/index.html', context=context)

    def post(self, request):
        pass


class DetailView(VerifyLoginView):
    '''
    详情
    '''

    def get(self, request, pk):

        # 获取详情id,不存在或者删除跳转回首页
        try:
            post = Post.objects.get(pk=pk, is_delete=False)
            # 阅读量 +1
            post.increase_views()
            post.body = markdown.markdown(post.body,
                                          extensions=[
                                              'markdown.extensions.extra',
                                              'markdown.extensions.codehilite',
                                              'markdown.extensions.toc',
                                          ])
        except Post.DoesNotExist:
            return redirect('blog:首页')

        # 获取这篇 post 下的全部评论
        comments = post.comment_set.all()

        # 将文章、表单、以及文章下的评论列表作为模板变量传给 detail.html 模板，以便渲染相应数据。
        comment_list = Comment.objects.filter(post_id=pk, is_delete=False)

        context = {'post': post,
                   'comment_list': comment_list,
                   'comments': comments,
                   }
        return render(request, 'blog/single.html', context=context)

    def post(self, request):
        pass


class ArchivesView(View):
    '''
    归档
    '''

    def get(self, request, year, month):
        # 获取归档年月,不存在或者删除跳转回首页
        try:
            post_list = Post.objects.filter(created_time__year=year,
                                            created_time__month=month,
                                            is_delete=False
                                            ).order_by('-created_time')
        except Post.DoesNotExist:
            return redirect('blog:首页')

        context = {
            'post_list': post_list
        }
        return render(request, 'blog/index.html', context=context)

    def post(self, request):
        pass


class TagView(ListView):
    '''
      标签云
    '''
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)



class CategoryView(View):
    '''
    分类
    '''

    def get(self, request, pk):
        # 获取分类,不存在或者删除跳转回首页
        try:
            cate = Category.objects.filter(pk=pk)
            post_list = Post.objects.filter(category=cate, is_delete=False).order_by('-created_time')
        except Post.DoesNotExist:
            return redirect('blog:首页')

        context = {
            'post_list': post_list
        }
        return render(request, 'blog/index.html', context=context)

    def post(self, request):
        pass


class BlogView(View):
    '''
    博客
    '''

    def get(self, request):
        post_list = Post.objects.filter(is_delete=False).order_by('-created_time')

        # 分页
        paginator = Paginator(post_list, 5)  # 每页显示n条记录
        # 获取当前页码数据
        page = request.GET.get('page', 1)  # 当前页码?Page=1
        # 获取对应页码数据
        try:
            post_list = paginator.page(page)
        except PageNotAnInteger:
            # 页码不是整数 显示第一页
            post_list = paginator.page(1)
        except EmptyPage:
            # 页码为空 显示最后一页
            post_list = paginator.page(paginator.num_pages)
        context = {
            'post_list': post_list
        }
        return render(request, 'blog/full-width.html', context=context)

    def post(self, request):
        pass


class AboutView(View):
    '''
    关于
    '''

    def get(self, request):
        return render(request, 'blog/about.html')

    def post(self, request):
        pass


class ContactView(VerifyLoginView):
    '''
    联系
    '''

    def get(self, request):
        return render(request, 'blog/contact.html')

    def post(self, request):
        pass
