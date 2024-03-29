from django.shortcuts import render,redirect
from . import models, forms
from .util import *
# Create your views here.

##加密密码
import hashlib
def hash_code(s,salt = 'mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def index(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, 'user/index.html')

def login(request):
    if request.session.get('is_login',None):
        return redirect('/index/')
    
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')



            try:
                user = models.User.objects.get(name=username)
            except :
                message = '用户不存在！'
                return render(request, 'user/login.html', locals())

            if user.pwd == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/index/')
            else:
                message = '密码不正确！'
                return render(request, 'user/login.html', locals())
        else:
            return render(request, 'user/login.html', locals())
    # 通过forms中的类将变量传给html
    login_form = forms.UserForm()
    return render(request, 'user/login.html', locals())


def logout(request):
    if not request.session.get('is_login',None):
        return redirect('/login/')
    request.session.flush()

    return redirect('/logout/')


def register(request):
    if request.session.get('is_login',None):
        return redirect('/index/')
    
    if request.method == 'POST':
        print('in post')
        register_form = forms.RegisterForm(request.POST)
        message = '输入不合法！'
        
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            pwd1 = register_form.cleaned_data.get('password1')
            pwd2 = register_form.cleaned_data.get('password2')
            type = register_form.cleaned_data.get('type')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')
            phoneNumber = register_form.cleaned_data.get('phoneNumber')
            # 检测输入密码是否一致
            if pwd1 != pwd2:
                message = '两次密码不同！'
                return render(request,'user/register.html', locals())
            elif len(pwd1) == 0:
                message = '密码不能为空！'
                return render(request,'user/register.html',locals())
            elif not judge_Monile_phone(phoneNumber):
                message = '手机号格式错误！'
                return render(request,'user/register.html',locals())

            # 检查身份，是否重复
            else:
                same_user = models.User.objects.filter(name=username)
                if same_user:
                    message = '用户名已存在！'
                    return render(request,'user/register.html',locals())
                same_email = models.User.objects.filter(email=email)
                if same_email:
                    message = '邮箱已存在！'
                    return render(request,'user/register.html',locals())
                new_user = models.User()
                new_user.name = username
                new_user.pwd = hash_code(pwd1)
                new_user.email = email
                new_user.sex = sex
                new_user.type = type
                new_user.save()
                return redirect('/login/')
        #注册表无效
        else:
            return render(request,'user/register.html',locals())

    register_form = forms.RegisterForm()
    return render(request, 'user/register.html',locals())


from django.views.generic import View
from django.http import HttpResponse

class UploadGoodsView(View):
    # 如果是GET请求，直接渲染到上传文件页面
    def get(self, request):
        return render(request, 'user/test.html')
    # 如果是POST请求，那么将接收文件的值
    def post(self, request):
        # 获取前台传来的文件，request.POST用来接收title和content，request.FILES用来接收文件
        form = forms.ArticleForm(request.POST, request.FILES)
        # 将数据保存到数据库orm cl
        if form.is_valid():
            print('clean data',form.cleaned_data)
            form.save()
            return HttpResponse("SUCCESS")
        else:
            # 打印错误信息
            print(form.errors.get_json_data())
            return HttpResponse("Fail")
class Upload(View):
    # 如果是GET请求，直接渲染到上传文件页面
    def get(self, request):
        form = forms.Upload()
        return render(request, 'user/uploadgoods.html',locals())
    # 如果是POST请求，那么将接收文件的值
    def post(self, request):
        # 获取前台传来的文件，request.POST用来接收title和content，request.FILES用来接收文件
        form = forms.Upload(request.POST, request.FILES)
        # 将数据保存到数据库
        if form.is_valid():
            newgoods = form.save(commit=False)
            seller = models.User.objects.get(pk=4)
            print('seller',seller)
            newgoods.seler_id = 4
            newgoods.save()
            return HttpResponse("上传成功")
        else:
            # 打印错误信息
            print(form.errors.get_json_data())
            return HttpResponse("上传失败")






