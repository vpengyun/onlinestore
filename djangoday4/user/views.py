from captcha.models import CaptchaStore
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
# from django.contrib.auth.views import logout
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.middleware.security import SecurityMiddleware
from django.middleware.csrf import CsrfViewMiddleware
# Create your views here.
from django.urls import reverse

from article.models import Article
from user.forms import UserRegisterForm, RegisterForm, LoginForm, CaptchaTestForm
from user.models import UserProfile
from user.utils import util_sendmsg, send_email, upload_image


def index(request):
    farticles = Article.objects.all().order_by('-click_num')
    darticles = Article.objects.all().order_by('-date')[:8]
    return render(request, 'index.html', context={'figure_articles': farticles[:3], 'darticles': darticles})


# 注册
def user_register(request):
    if request.method == 'GET':
        return render(request, 'user/register.html')
    else:
        rform = RegisterForm(request.POST)  # 使用form获取数据
        if rform.is_valid():  # 进行数据的校验
            # 从干净的数据中取值
            username = rform.cleaned_data.get('username')
            email = rform.cleaned_data.get('email')
            mobile = rform.cleaned_data.get('mobile')
            password = rform.cleaned_data.get('password')
            if not UserProfile.objects.filter(Q(username=username) | Q(mobile=mobile)).exists():
                # 注册到数据库中
                password = make_password(password)  # 密码加密
                user = UserProfile.objects.create(username=username, password=password, email=email, mobile=mobile)
                if user:
                    return HttpResponse('注册成功')
            else:
                return render(request, 'user/register.html', context={'msg': '用户名或者手机号码已经存在！'})
        return render(request, 'user/register.html', context={'msg': '注册失败，重新填写！'})


# 用户登录
def user_login(request):
    if request.method == 'GET':
        return render(request, 'user/login.html')
    else:
        lform = LoginForm(request.POST)
        if lform.is_valid():
            username = lform.cleaned_data.get('username')
            password = lform.cleaned_data.get('password')
            # 进行数据库的查询
            # user = UserProfile.objects.filter(username=username).first()
            # flag = check_password(password, user.password)
            # if flag:
            #     # 保存session信息
            #     request.session['username'] = username

            # 方式二前提是继承了AbstractUser
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)  # 将用户对象保存在底层的request中  （session）

                return redirect(reverse('index'))
        return render(request, 'user/login.html', context={'errors': lform.errors})


# 用户注销
def user_logout(request):
    # request.session.clear()  # 删除字典
    # request.session.flush()  # 删除django_session + cookie +字典
    logout(request)

    return redirect(reverse('index'))


# 手机验证码登录
def code_login(request):
    if request.method == 'GET':
        return render(request, 'user/codelogin.html')
    else:
        mobile = request.POST.get('mobile')
        code = request.POST.get('code')

        # 根据mobile去session中取值
        check_code = request.session.get(mobile)
        if code == check_code:
            user = UserProfile.objects.filter(mobile=mobile).first()
            # user = authenticate(username=user.username, password=user.password)
            print(user)
            if user:
                login(request, user)
                return redirect(reverse('index'))
            else:
                return HttpResponse('验证失败！')
        else:
            return render(request, 'user/codelogin.html', context={'msg': '验证码有误！'})


# 发送验证码路由  ajax发过来的请求
def send_code(request):
    mobile = request.GET.get('mobile')
    data = {}
    if UserProfile.objects.filter(mobile=mobile).exists():
        # 发送验证码  第三方
        json_result = util_sendmsg(mobile)
        # 取值：
        status = json_result.get('code')
        if status == 200:
            check_code = json_result.get('obj')
            # 使用session保存
            request.session[mobile] = check_code

            data['status'] = 200
            data['msg'] = '验证码发送成功'
        else:
            data['status'] = 500
            data['msg'] = '验证码发送失败'
    else:
        data['status'] = 501
        data['msg'] = '用户不存在'

    return JsonResponse(data)


# 忘记密码
def forget_password(request):
    if request.method == 'GET':
        form = CaptchaTestForm()
        return render(request, 'user/forget_pwd.html', context={'form': form})
    else:
        # 获取提交的邮箱，发送邮件，通过发送的邮箱链接设置新的密码
        email = request.POST.get('email')
        # 给此邮箱地址发送邮件
        result = send_email(email, request)
        if result:
            return HttpResponse("邮件发送成功！赶快去邮箱更改密码！<a href='/'>返回首页>>> </a>")


# 更新密码
def update_pwd(request):
    if request.method == 'GET':
        c = request.GET.get('c')
        return render(request, 'user/update_pwd.html', context={'c': c})
    else:
        code = request.POST.get('code')
        uid = request.session.get(code)
        user = UserProfile.objects.get(pk=uid)
        # 获取密码
        pwd = request.POST.get('password')
        repwd = request.POST.get('repassword')
        if pwd == repwd and user:
            pwd = make_password(pwd)
            user.password = pwd
            user.save()
            return render(request, 'user/update_pwd.html', context={'msg': '用户密码更新成功！'})
        else:
            return render(request, 'user/update_pwd.html', context={'msg': '更新失败！'})


# 定义一个路由验证验证码
def valide_code(request):
    if request.is_ajax():
        key = request.GET.get('key')
        code = request.GET.get('code')

        captche = CaptchaStore.objects.filter(hashkey=key).first()
        if captche.response == code.lower():
            # 正确
            data = {'status': 1}
        else:
            # 错误的
            data = {'status': 0}
        return JsonResponse(data)


# 用户的个人中心  login(request,user)   user--->继承自abstractuser
@login_required
def user_center(request):
    user = request.user
    if request.method == 'GET':

        return render(request, 'user/center.html', context={'user': user})
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        icon = request.FILES.get('icon')
        # print(type(icon))
        # print(icon.name)
        # print(icon.read())
        # 更新用户
        user.username = username
        user.email = email
        user.mobile = mobile
        user.icon = icon  # ImageField(upload_to='')
        user.save()

        return render(request, 'user/center.html', context={'user': user})


@login_required
def user_center1(request):
    user = request.user
    if request.method == 'GET':

        return render(request, 'user/center.html', context={'user': user})
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        icon = request.FILES.get('icon')  # 内存存储对象

        user.username = username
        user.email = email
        user.mobile = mobile

        # print(str(user.icon),type(user.icon))
        # 上传图片到七牛云
        save_path = upload_image(icon)
        user.yunicon = save_path
        user.save()

        return render(request, 'user/center.html', context={'user': user})


# from  django.db.models.fields.files import ImageFieldFile

def test(request):
    return render(request, 'article/info.html')


def user_zhuce(request):
    if request.method == 'GET':
        rform = RegisterForm()
        return render(request, 'user/zhuce.html', context={'rform': rform})
    else:
        rform = UserRegisterForm(request.POST)
        if rform.is_valid():
            print(rform.cleaned_data)
            username = rform.cleaned_data.get('username')
            email = rform.cleaned_data.get('email')
            mobile = rform.cleaned_data.get('mobile')
            password = rform.cleaned_data.get('password')

            # 数据库中注册
        return HttpResponse('yiui')
