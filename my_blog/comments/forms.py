from captcha.fields import CaptchaField
from django import forms
from comments.helper import set_password
from comments.models import Users, Comment


# 评论
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


# 注册
class RegisterForm(forms.Form):
    nickname = forms.CharField(max_length=10,
                               min_length=2,
                               error_messages={'required': '请填写昵称!',
                                               'min_length': '请输入至少两个字符!',
                                               'max_length': '请输入小于或等于十十个字符!'
                                               },
                               )
    email = forms.CharField(error_messages={
        'required': '请输入邮箱!'
    },
    )
    password = forms.CharField(max_length=20,
                               min_length=6,
                               error_messages={
                                   'required': '请填写密码!',
                                   'min_length': '请输入至少六个字符!',
                                   'max_length': '请输入小于或等于二十个字符!'
                               })
    repassword = forms.CharField(max_length=20,
                                 min_length=6,
                                 error_messages={
                                     'required': '这是必填选项!',
                                     'min_length': '请输入至少六个字符!',
                                     'max_length': '请输入小于或等于二十个字符!'
                                 })
    # invalid 表示出错时候的显示信息.
    captcha = CaptchaField()


    def clean(self):
        pwd = self.cleaned_data.get("password")  # 密码
        repwd = self.cleaned_data.get("repassword")  # 重复密码
        if pwd and repwd and pwd != repwd:
            raise forms.ValidationError({"repassword": "两次密码不一致,请重新输入!"})

    def clean_email(self):  # 验证用户名是否重复
        email = self.cleaned_data.get('email')
        flag = Users.objects.filter(email=email).exists()
        if flag:
            # 存在 错误
            raise forms.ValidationError("该邮箱已注册,请直接登录!")
        else:
            return email


# 登录
class LoginForm(forms.Form):
    email = forms.CharField(error_messages={
        'required': '请输入邮箱!'
    },
    )
    password = forms.CharField(max_length=20,
                               min_length=6,
                               error_messages={
                                   'required': '请填写密码!',
                                   'min_length': '请输入至少六个字符!',
                                   'max_length': '请输入小于或等于二十个字符!'
                               })
    # invalid 表示出错时候的显示信息.
    captcha = CaptchaField()

    def clean(self):
        # 验证用户名
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        # 验证手机号
        try:
            user = Users.objects.get(email=email)
        except Users.DoesNotExist:
            raise forms.ValidationError({'email': '邮箱错误'})
        # 验证密码
        if user.password != set_password(password):
            raise forms.ValidationError({'password': '密码填写错误'})

        # 用于session验证登录
        self.cleaned_data['user'] = user
        # 返回,返回整个清洗后的数据
        return self.cleaned_data
