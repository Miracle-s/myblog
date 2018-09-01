from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from blog.models import Category,ArticleColumn,Article
from .forms import LoginForm,RegisterForm,UserInfoForm
from django.contrib.auth import authenticate, login
from .models import Code,UserInfo
# Create your views here.
import base64
from itsdangerous import URLSafeTimedSerializer as utsr
from django.conf import settings as django_settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from blog.views import pageFunc
from django.views.decorators.csrf import csrf_exempt


class Token:
    def __init__(self, security_key):
        self.security_key = security_key
        self.salt = base64.encodestring(security_key)
    def generate_validate_token(self, username):
        serializer = utsr(self.security_key)
        return serializer.dumps(username, self.salt)
    def confirm_validate_token(self, token, expiration=3600):
        serializer = utsr(self.security_key)
        return serializer.loads(token, salt=self.salt, max_age=expiration)
    def remove_validate_token(self, token):
        serializer = utsr(self.security_key)
        return serializer.loads(token, salt=self.salt)

token_confirm = Token(django_settings.SECRET_KEY.encode('utf-8'))


def active_user(request, token):
    try:
        username = token_confirm.confirm_validate_token(token)
    except:
        username = token_confirm.remove_validate_token(token)
        users = User.objects.filter(username=username)
        for user in users:
            user.delete()
        return render(request, 'account/message.html', {'message': '对不起，验证链接已经过期，请重新<a href=\"' + django_settings.DOMAIN + 'account/register\">注册</a>'})
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, 'account/message.html', {'message': "对不起，您所验证的用户不存在，请重新注册"})
    user.is_active = True
    user.save()
    categorys = Category.objects.all() 
    message = {'result':'验证成功','address':'http://192.168.187.148:8000/account/login','word':'登录','other':'操作'}
    return render(request, 'account/message.html', {'message':message})

def home(request):
    return HttpResponse("hhhh")

def password_change_done(request):
    message = "恭喜！修改密码成功！！"
    return render(request, 'account/message.html', {"message":message})

def signin(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username=cd['username'],password=cd['password'])
            if user:
                login(request,user)
                message = "登录成功！！"
                return render(request, "account/message.html", {"message":message})
            else:
                errors = "用户名或密码不正确！"
                return render(request, "account/login.html", {"form":login_form, "errors":errors})
        else:
            errors = "输入不合法！"
            return render(request, "account/login.html", {"form":login_form, "errors":errors})
    elif request.method == "GET":
        if request.user.is_authenticated():
            message = "已的登录，若切换用户请先退出登录"
            return render(request, "account/message.html",{"message":message})
        login_form = LoginForm()
        return render(request, "account/login.html", {"form":login_form})

def signup(request):
    if request.method == "POST":
        user_form = RegisterForm(request.POST)
        codes = Code.objects.all()
        codess = []
        for item in codes:
            codess.append(item.code)
        if user_form.is_valid():
            code = user_form.cleaned_data['code']      
            if code not in codess or Code.objects.get(code=code).is_used:
                    return render(request,'account/register.html',{'form':user_form})

            new_user = user_form.save(commit=False)
            new_user.username = user_form.cleaned_data['username']
            new_user.email = user_form.cleaned_data['email']
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.is_activite = False
            new_user.code = code
            code = Code.objects.get(code=code)
            #code.is_used = True
            #code.save()
            new_user.save()
            UserInfo.objects.create(user=new_user)
            token = token_confirm.generate_validate_token(new_user.username)
            message = "\n".join(['{},欢迎加入博客家园'.format(new_user.username),'请访问该连接，完成用户认证：','/'.join([django_settings.DOMAIN,':8000','account/activate',token])])
            send_mail('注册用户验证信息',message,'18591838081@163.com',[new_user.email],fail_silently=False)
            message = '请登录邮箱进行身份验证！！'
            return render(request,'account/message.html',{'redirect_url':'home.html','message':message})
        else:
            return render(request,"account/register.html",{'form':user_form})
    elif request.method == "GET":
        if request.user.is_authenticated():
            message = "用户已登录，若要注册请先退出登录！！"
            return render(request, 'account/message.html',{"message":message})
        register_form = RegisterForm()
        return render(request, "account/register.html",{"form":register_form})


@login_required(login_url='/account/login/')
def my_info(request):
    username = request.user.username
    email = request.user.email
    userInfo = request.user.userinfo
    return render(request, 'account/my_info.html',{"username":username, "email":email, "userInfo":userInfo})


@login_required(login_url="/account/login/")
def my_info_edit(request):
    username = request.user.username
    email = request.user.email
    userinfo = UserInfo.objects.filter(user=request.user).first()
    photo = userinfo.photo
    if request.method == "POST":
        userinfo_form = UserInfoForm(request.POST)
        if userinfo_form.is_valid():
            cd = userinfo_form.cleaned_data
            userinfo.phone = cd['phone']
            userinfo.school = cd['school']
            userinfo.compay = cd['company']
            userinfo.profession = cd['profession']
            userinfo.address = cd['address']
            userinfo.aboutme = cd['aboutme']
            userinfo.save()
            return HttpResponseRedirect('/account/my-info-edit')
        return render(request,'account/my_info_edit.html',{'username':username,'email':email,'photo':photo,'userinfo_form':userinfo_form})
    else:
        userinfo_form = UserInfoForm(initial={"phone":userinfo.phone,"school":userinfo.school,"company":userinfo.company,"profession":userinfo.profession,"address":userinfo.address,"aboutme":userinfo.aboutme})
        
        return render(request, 'account/my_info_edit.html',{'username':username,'email':email,'photo':photo,'userinfo_form':userinfo_form})
        

@login_required(login_url="/account/login/")
def my_image(request):
    if request.method == "POST":
        userinfo = UserInfo.objects.filter(user=request.user).first()
        userinfo.photo = request.POST['img']
        userinfo.save()
        return HttpResponse('1')
    else:
        return render(request,'account/imagecrop.html')


@login_required(login_url="/account/login/")
def my_blog_list(request, column_id):
    columns = request.user.article_column.all()
    if columns:
        try:
            column = ArticleColumn.objects.get(id=column_id)
        except:
            column = columns.first()
        articles = column.article.filter(author=request.user)
        cus_list = pageFunc(request,articles)
        return render(request, "account/my_blog_list.html",{"columns":columns, "column":column, "cus_list":cus_list,"articles":cus_list})
    info_column = "抱歉！该作者没有写任何文章，请留言提醒！！"
    return render(request, "account/my_blog_list.html",{"columns":columns, "column":column, "info_column":info_column})    

@csrf_exempt
def blog_remove(request):
    if request.method == "POST":
        print(request.POST['article_id'])
        return HttpResponse('hhhhhh')
