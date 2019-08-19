mtv:
m model
数据库


class ArticleManager(models.Manager):
    重写：
    def get_queryset(self):

        return super(xxxx,self).get_querySet().filter(isdelete=False)

class User(models.Model):
     属性

     objects= ArticleManager()

     objects1= models.Manager()

     class Meta:
        ..


User.objects----->  查询的是isdelete=False 没有删除删除的文章

User.objects1.all()   ----> 查询的就是所有的文章


查询：
filter(name__contains='')
filter(age__gte=19)
filter()
Article.objects.filter(tag__name__contains='')

filter().filter().filter()
filter().order_by('-age')
filter().count()
filter().exists()
filter().first()
....

filter(Q() | Q())
filter( save_num__gt= F(love_num))


1对1 ： OneToOneField（to= ,on_delete=models.xxxx） ~   ForeignKey(to=,on_delete= ,unique=True)

1对多： ForeignKey(to=,on_delete=)

       正向： user.article_set.all()

       反向: article.user
多对多：
       ManyToManyField(to=)   ----> 自动产生关系表
       Article ----》 tags = ManyToManyField(to=)

       正向： article.tags

       反向:  tags.article_set


       添加：
        article.tags.add(tag)

       删除：
       article.tags.remove(tag)
       article.tags.clear()

文件上传：设置model
media文件： 文件上传的文件

模型： FileField（任何文件）  ImageField（只能是图片）继承自FileField

FileField(upload_to='表示文件上传的路径 uploads/%Y/%m')

ImageField(upload_to='相对路径')

此路径是基于media_root指明的路径。

在settings.py 文件中配置：
MEDIA_URL = '/static/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')
static
  |-- media
       |--  uploads
               |---2019
                     |---05
                         |---文件名

模板中如果想引用上传的文件，并显示：
就需要在settings.py ---->TEMPLATES--->  'context_processors': [  ]---> 添加：django.template.context_processors.media


二、
系统默认用户的继承使用：
1. 必须继承AbstractUser   ----》auth_user ----> 系统用户
class UserProfile(AbstractUser):
    mobile = models.CharField(max_length=11, verbose_name='手机号码', unique=True)
    icon = models.ImageField(upload_to='uploads/%Y/%m/%d')

    class Meta:
        db_table = 'userprofile'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name
2. 必须修改settings.py
  添加：
  # 如果用户继承了AbstractUser，修改auth_user的模型
  AUTH_USER_MODEL = 'user.UserProfile'

3. 然后执行迁移和同步



authenticate() （认证）---》user =====》  login(request,user)---->  session保存和request.user赋值

logout()----》清空session和cookie，将request.user设置成匿名的User()

is_authenticated() ----> 判断用户是否被认证   request.user.is_authenticated()



三、
forms 表单：
Django会处理涉及表单的三个不同部分：
    准备并重组数据，以便下一步的渲染
    为数据创建HTML 表单
    接收并处理客户端提交的表单及数据

使用： Form 和  ModelForm
Form比较灵活需要自己定义各个要验证的字段
ModelForm是跟Model有关的，model的字段可以直接引用过来。

Form使用：
class UserRegisterForm(Form):
    username = forms.CharField(max_length=50, min_length=6, error_messages={'min_length': '用户名长度至少6位', }, label='用户名')
    email = forms.EmailField(required=True, error_messages={'required': '必须填写邮箱信息'}, label='邮箱')
    mobile = forms.CharField(required=True, error_messages={'required': '必须填写手机号码'}, label='手机')
    password = forms.CharField(required=True, error_messages={'required': '必须填写密码'}, label='密码',
                               widget=forms.widgets.PasswordInput)


ModelForm使用：
class RegisterForm(ModelForm):
    repassword = forms.CharField(required=True, error_messages={'required': '必须填写确认密码'}, label='确认密码',
                                              widget=forms.widgets.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'mobile', 'password']  ---->可以自己添加需要验证的字段
        # fields = '__all__'   ----》 如果是model中的所有字段都需要验证可以使用__all__
        # exclude = ['first_name','date_joined','last_name']   -----> 使用exclude排除不需要验证的部分


另外还可以定义一些指定字段的专门验证：
  def clean_username(self):
        username = self.cleaned_data.get('username')
        result = re.match(r'[a-zA-Z]\w{5,}', username)
        if not result:
            raise ValidationError('用户名必须字母开头')
        return username

或者

  def clean_username(self):
        username = self.cleaned_data.get('username')
        if not UserProfile.objects.filter(username=username).exists():
            raise ValidationError('用户名不存在')
        return username

或者验证密码与确认密码是否一致

    def clean_password(self):
         repassword = self.cleaned_data.get('repassword')
         password = self.cleaned_data.get('psssword')
         if password != repassword:
              raise ValidationError('密码不一致')
         return password



4. 密码加密和检查密码：
   check_password(原文密码，加密密码) -----》返回结果是boolean
   make_password(原文密码)  -----》加密密码返回结果是加密后的密码



5. session的使用：
    request.session  request里面的一个属性，而且是字典类型

    request.session设置session的值
    设置
    request.session['key']=value

    取值
    value = request.session.get(key)

    清除session
    request.session.clear()  # 删除字典
    request.session.flush()  # 删除django_session + cookie +字典

    del request.session[key] # 删除指定的key



 继承abstractuser

  logout, 注销用户

  authenticate+login  先使用authenticate 进行用户的数据库查询判断，如果有则返回用户对象

  login(request,user)   ---->类似session  只不过： request.user=user

  request.user.is_authenticated  是否是认证过的用户返回值是True，False

5月7日：
一、发送手机验证码：第三方

发送验证码  ---》 send_code ----> ajax ----》sendcode  + mobile
-----》后台：mobile  -----》使用requests（浏览器）
url ='' ---->访问网易云信的url地址
data={'mobile':你的手机号码}  ---->
headers={} -----》4 部分
AppKey =‘’
Nonce=‘’
CurTime=时间戳
CheckSum=sha1（appsecret+Nonce+CurTime）
response = requests.post(url,data,headers)

str = response.Text
json = json.loads(str)

json.code
json.obj   ----> 发送的验证码

保存到session

验证码登录

二、生成图形验证码
使用插件验证码：

Install django-simple-captcha via pip: pip install  django-simple-captcha

Add captcha to the INSTALLED_APPS in your settings.py

Run python manage.py migrate------》数据库： captcha-captchastore

Add an entry to your urls.py:

如何使用验证码插件？

Form使用
# 验证码captcha的Form
class CaptchaTestForm(forms.Form):
    email = EmailField(required=True, error_messages={'required': '必须填写邮箱'},label='邮箱')
    captcha = CaptchaField()

产生的图形就是一张图片。img+hidden

使用CaptchaTestForm渲染页面：
 if request.method == 'GET':
        form = CaptchaTestForm()
        return render(request, 'user/forget_pwd.html', context={'form': form})

页面中使用captcha：
<div class="w3layouts-main">
                <p>{{ msg }} {{ errors }}</p>
                <form action="{% url 'user:forget_pwd' %}" method="post"> {% csrf_token %}
                    {{ form.email }}
                    {{ form.captcha }}
                    <input type="submit" value="找回密码">
                </form>
            </div>

动作：
1.刷新验证：
  // 刷新动作
        $('.captcha').click(function(){
            var img= $(this);
           $.getJSON('/captcha/refresh',function(data){
               console.log(data)
               img.attr('src',data['image_url']);
               $('#id_captcha_0').val(data['key'])
           })
        });

2. 验证验证码是否正确
 // 验证验证码是否正确
          $('#id_captcha_1').blur(function(){
              var $this = $(this);
              var key = $('#id_captcha_0').val();
              var code = $(this).val();

              $.getJSON('{% url 'user:valide_code' %}',{key:key,code:code},function(data){
                    console.log(data)

                  if(data.status==1){
                    $this.after('<span>验证码正确</span>')
                  }else{
                    $this.after('<span>验证码错误</span>')
                  }
              })
          })

路由：valide_code

# 定义一个路由验证验证码
def valide_code(request):
    if request.is_ajax():
        key = request.GET.get('key')
        code = request.GET.get('code')
        # CaptchaStore 模型对象
        captche = CaptchaStore.objects.filter(hashkey=key).first()
        if captche.response == code.lower():
            # 正确
            data = {'status': 1}
        else:
            # 错误的
            data = {'status': 0}
        return JsonResponse(data)


三、发送邮件
找回密码：
发送邮件

邮件的配置：
EMAIL_HOST = 'smtp.126.com'
EMAIL_HOST_USER = 'student1902@126.com'
EMAIL_HOST_PASSWORD = 'student1902'
EMAIL_PORT = 25
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False   # 126,QQ: 465   163:454


调用方法：
send_mail(subject,message,from,to_list)

发送成功就是1  否则0

message与html_message的区别

     ran_code = uuid.uuid4()
     ran_code = str(ran_code)

    ran_code =ran_code.replace('-','')
    request.session[ran_code] = user.id


进行激活：
密码和确认密码+ 隐藏表单域（code）

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
            return render(request, 'user/update_pwd.html', context={'msg':'用户密码更新成功！'})
        else:
            return render(request, 'user/update_pwd.html', context={'msg': '更新失败！'})



5月8日：

一、中间件（类似flask 钩子函数）

    中间件应用场景
    由于中间件工作在 视图函数执行前、执行后适合所有的请求/一部分请求做批量处理。
    1、做IP限制
    放在中间件类的列表中，阻止某些IP访问了；
    2.URL访问过滤
    如果用户访问的是login视图（放过）
    如果访问其他视图（需要检测是不是有session已经有了放行，没有返回login），这样就省得在 多个视图函数上写装饰器了！
    3、缓存(CDN)
    客户端请求来了，中间件去缓存看看有没有数据，有直接返回给用户，没有再去逻辑层 执行视图函数




   进行用户的登录验证

   方式：
   一.中间件的请求路径验证用户登录
     步骤：
     1. 文件夹----》 xxxmiddleware.py ---->定义类继承MiddlewareMixin

     2. 重写：

         如果仅仅是对请求做处理则重写的方法名：process_request(self,request)

     3. 参数request：参数request是请求对象
        request.path
        request.method
        request.is_ajax()
        request.META.get('REMOTE_ADDR')

        if path in login_list:
            print(request.user)  # AnonymousUser  未登录
            print(type(request.user))
            print(request.user.username)   # 认为就是用户登录的对象
            if not request.user.is_authenticated:
                return redirect(reverse('user:login'))



    二、使用装饰器：
      @login_required  前提（要验证的用户必须是继承自AbstractUser）

      login(request,user)

      request.user.is_authenticated

        @login_required
        def user_center(request):
            return HttpResponse('用户中心')

        改变页面跳转
        就需要在settings.py文件中设置:
        # 添加一个登陆路由  结合  @login_required
        LOGIN_URL = '/user/login'


中间件的默认可以自定义的函数：
Request预处理函数: process_request(self, request)
    这个方法的调用时机在Django接收到request之后，但仍未解析URL以确定应当运行的视图函数。Django向它传入相应的Request对象，以便在方法中修改。
    如果返回None，Django将继续处理这个request，执行后续的中间件， 然后调用相应的 view。
    如果返回HttpResponse对象，Django将不再执行任何除了process_response以外其它的中间件以及相应的view，Django将立即返回该HttpResponse。

View预处理函数: process_view(self, request, callback, callback_args,callback_kwargs)
    这个方法的调用时机在 Django 执行完 request 预处理函数并确定待执行的 view （即callback参数）之后，但在 view 函数实际执行之前。
    request：HttpRequest 对象。
    callback：Django将调用的处理request的python函数. 这是实际的函数对象本身, 而不是字符串表述的函数名。
    args：将传入view的位置参数列表，但不包括request参数(它通常是传入view的第一个参数)。
    kwargs：将传入view的关键字参数字典。
    process_view() 应当返回None或 HttpResponse 对象。如果返回 None， Django将继续处理这个request ，执行后续的中间件， 然后调用相应的view。
    如果返回 HttpResponse 对象，Django 将不再执行任何其它的中间件(不论种类)以及相应的view，Django将立即返回。


Template模版渲染函数：process_template_response()
    默认不执行，只有在视图函数的返回结果对象中有render方法才会执行，并把对象的render方法的返回值返回给用户
    （注意不返回视图函数的return的结果了，而是返回视图函数 return值（对象）中rende方法的结果）

Exception后处理函数:process_exception(self, request, exception)
    这个方法只有在 request 处理过程中出了问题并且view 函数抛出了一个未捕获的异常时才会被调用。这个钩子可以用来发送错误通知，将现场相关信息输出到日志文件，或者甚至尝试从错误中自动恢复。
    这个函数的参数除了一贯的request对象之外，还包括view函数抛出的实际的异常对象exception 。
    process_exception() 应当返回None或HttpResponse对象。
    如果返回None，Django将用框架内置的异常处理机制继续处理相应request。
    如果返回HttpResponse对象，Django将使用该response对象，而短路框架内置的异常处理机制。

Response后处理函数:process_response(self, request, response)
    这个方法的调用时机在 Django 执行 view 函数并生成 response 之后。
    该处理器能修改response 的内容；一个常见的用途是内容压缩，如gzip所请求的HTML页面。
    这个方法的参数相当直观：request是request对象，而response则是从view中返回的response对象。
    process_response() 必须返回 HttpResponse 对象. 这个 response 对象可以是传入函数的那一个原始对象（通常已被修改），也可以是全新生成的

过程参看这张图片：
https://upload-images.jianshu.io/upload_images/3269979-f2a500b0294f850c?imageMogr2/auto-orient/strip%7CimageView2/2/w/580
https://images2015.cnblogs.com/blog/997599/201701/997599-20170113093429385-1950865037.png
https://images2015.cnblogs.com/blog/997599/201701/997599-20170113093451697-1784079574.png



二、图片上传；

显示：
使用媒体文件显示：
 1. settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

2. 添加：
识别：{{ MEDIA_URL }}
在模板中添加：
'django.template.context_processors.media',  # 在模板中可以使用{{ MEDIA_URL }}

3.配置路由：
在主路由中添加：
 re_path(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT})

4. <img src="{{ MEDIA_URL }}{{ user.icon }}" alt="" id="icon">




icon = models.ImageField(upload_to='uploads/%Y/%m/%d', default="uploads/mine1.png")

如果使用ImageField完成文件上传：
        icon = request.FILES.get('icon')  -----> 内存 的存储对象
        user.username = username
        user.email = email
        user.mobile = mobile
        user.icon = icon  # ImageField(upload_to='')
        user.save()

        user.icon   ----> 不是存储字符串，ImageField
        user.icon.name  ----> 字符串值

三、云存储：
1. 注册用户
2. 创建存储空间，测试域名
3. 文档中心：https://developer.qiniu.com/kodo/sdk/1242/python
4. 在项目中使用：

def upload_image(storeobj):
    # 只要注册用户就会有默认的access_key，secret_key
    access_key = '1fXvG9wkbN7AgRUG6usHDcRP5Bb85apcovRAIITP'
    secret_key = 'Aqf1lPAmUG72EdZJ7PxKtWHfWDYNdUycZP1TaAIN'

    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = 'myblog'

    # 上传后保存的文件名
    key = storeobj.name

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)

    # 要上传文件的本地路径
    # localfile = os.path.join(MEDIA_ROOT, imagepath)  # 本地图片路径
    ret, info = put_data(token, key, storeobj.read())   # 第三个参数是二进制流
    ret,info = put_file(token,key,localfile) # 第三个参数是文件的路径

    print(ret, info)
    filename = ret.get('key')
    save_path = 'http://pr67kkhq9.bkt.clouddn.com/'+filename
    return save_path


5月9日：
1. xadmin与admin的区别：
  xadmin就是admin的升级版，样式，操作方便

  安装：
  pip install xadmin

  推荐源码安装：
  xxxdjango2.0-xadmin.zip
       |--django2.0-xadmin
            |--- xadmin
            |---requirements.txt

   1. pip install -r    requirements.txt

  2. xadmin复制到项目下
  3. 在settings.py
      INSTALLED_APPS=[
        'xadmin',
        'crispy_forms'
      ]
  4. URL访问：
    主路由：
       path('xadmin/',xadmin.site.urls)

  5.迁移和同步

  6. 看到model，就需要注册：

      你的app
         |--admin.py
         |--xadmin.py  -----> xadmin.site.register(xxxModel)

  7. 配置：
    class ArticleAdmin(object):
    list_display = ['title', 'click_num', 'love_num', 'user']
    search_fields= ['title','id']
    list_editable= ['click_num','love_num']
    list_filter=['date','user']


    xadmin.site.register(Article,ArticleAdmin)
    xadmin.site.register(Tag)


    class ArticleConfig(AppConfig):
        name = 'article'
        verbose_name = '文章操作'

    __init__.py
        |--- default_app_config = 'article.apps.ArticleConfig'

    主题设置：

        class BaseSettings(object):
            enable_themes = True
            use_bootswatch = True


        class GlobalSettings(object):
            site_title = '博客后台管理'
            site_footer = '达达的博客公司'


        xadmin.site.register(views.BaseAdminView, BaseSettings)
        xadmin.site.register(views.CommAdminView, GlobalSettings)


详情：


分页：Paginator，Page
    分页器：
    paginator = Paginator(articles, 3)  # Paginator(对象列表，每页几条记录)
    分页器属性：
    print(paginator.count)  # 总的条目数  总的记录数
    print(paginator.num_pages)  # 可以分页的数量  总的页码数
    print(paginator.page_range)  # 页面的范围


    # 方法： get_page()
    page = request.GET.get('page',1)
    page = paginator.get_page(page)   # 返回的是page对象   参数就是页码数

    # 方法：
    # page.has_next()  # 有没有下一页
    # page.has_previous()  # 判断是否存在前一页
    # page.next_page_number() # 获取下一页的页码数
    # page.previous_page_number() # 获取前一页的页码数

    #属性：
    # object_list   当前页的所有对象
    # number       当前的页码数
    # paginator     分页器对象



5月10日：

富文本：

ckeditor

步骤：
1. pip install django-ckeditor
2. 注册ckeditor应用
打开django项目的settings.py文件，在INSTALLED_APPS中加入'ckeditor'，如：
INSTALLED_APPS = [
    # ...
    'ckeditor',
]
3.文件上传需要：
INSTALLED_APPS = [
    # ...
    'ckeditor',
    'ckeditor_uploader'
]

文件上传配置:
配置MEDIA_URL和MEDIA_ROOT, 上传路径的根目录就是以MEDIA_ROOT
设置CKEDITOR_UPLOAD_PATH = "uploads/",

4.设置urls.py路径:
# 加载ckeditor的urls
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),

5.在models.py中设置：RichTextUploadingField
class Article(models.Model):
    title = models.CharField(max_length=100, verbose_name='标题')
    desc = models.CharField(max_length=256, verbose_name='简介')
    content = RichTextUploadingField(verbose_name='内容')

6.迁移和同步

7.访问：xadmin后台








