from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from blog.models import Post
from comments.forms import RegisterForm, LoginForm, CommentForm
from comments.helper import set_password, login
from comments.models import Users, Comment
from db.base_view import VerifyLoginView


class RegisterView(View):
    '''
    注册
    '''

    def get(self, request):

        return render(request, 'comments/register.html')

    def post(self, request):
        # 完成用户信息的注册
        # 接收参数
        data = request.POST
        # 验证参数合法性 表单验证
        form = RegisterForm(data)
        if form.is_valid():
            # 获取清洗后的数据
            cleaned = form.cleaned_data
            # 将密码进行加密
            # 取出清洗后的昵称
            nickname = cleaned.get('nickname')
            # 取出清洗后的邮箱
            email = cleaned.get('email')
            # 取出清洗后的密码
            password = set_password(cleaned.get('password'))
            # print(password)
            # 修改到数据库
            data = {'nickname': nickname,
                    'email': email,
                    'password': password}
            Users.objects.create(**data)
            # 跳转到登录页
            return redirect('comments:登录')
        else:
            # 错误
            context = {
                'errors': form.errors,
            }
            return render(request, 'comments/register.html', context=context)


class LogintView(View):
    '''
    登录
    '''

    def get(self, request):
        return render(request, 'comments/login.html')

    def post(self, request):
        # 接收参数
        data = request.POST

        # 验证数据的合法性
        form = LoginForm(data)
        if form.is_valid():
            # session验证登录
            user = form.cleaned_data.get('user')
            login(request, user)
            # 获取清洗后的数据
            cleaned = form.cleaned_data
            # 将密码进行加密
            # 取出清洗后的手机号
            email = cleaned.get('email')
            # 取出清洗后的密码
            password = set_password(cleaned.get('password'))
            # 从数据库查询
            try:
                Users.objects.get(email=email, password=password)
                # 跳回以前页面
                referer = request.session.get('referer')
                if referer:
                    # 跳转回去
                    # 删除session
                    del request.session['referer']
                    return redirect(referer)
                else:
                    # 跳转到登录页
                    return redirect('blog:首页')
            except:
                return render(request, "comments/login.html")

        else:  # 不合法
            context = {
                'errors': form.errors,
            }
            return render(request, "comments/login.html", context=context)


class Post_commentView(VerifyLoginView):
    '''
    文章评论
    先获取被评论的文章，因为后面需要把评论和被评论的文章关联起来。
    '''

    def get(self, request):
        return render(request, 'comments/login.html')

    def post(self, request, post_pk):
        # 获取文章评论,不存在或者删除跳转回首页
        try:
            post = Post.objects.filter(pk=post_pk,
                                       is_delete=False
                                       )
        except Post.DoesNotExist:
            return redirect('blog:首页')

        # 接收参数
        data = request.POST
        form = CommentForm(data)

        # 接收用户的id
        user_id = request.session.get("ID")
        # 验证数据的合法性
        if form.is_valid():
            # 获取清洗后的数据
            cleaned = form.cleaned_data
            # 取出清洗后的评论
            text = cleaned.get('text')
            # 保存到数据库
            Comment.objects.create(text=text,post_id=post_pk,users_id=user_id)
            return render(request,'blog/full-width.html')
        else:
            return render(request, 'blog/full-width.html')

