from django.http import JsonResponse
from django.shortcuts import render,redirect
from . import models, forms
from .util import *
from django.views.generic import View
from django.http import HttpResponse

from django.contrib import messages
# Create your views here.

##加密密码
import hashlib
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
def hash_code(s,salt = 'mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def index(request):
    allgoods = models.Goods.objects.filter()
    if not request.session.get('is_login', None):
        return redirect('/login/')
    if request.session['user_type'] == 0:
        return render(request, 'user/base_buyer.html',locals())
    elif request.session['user_type'] == 1:
        return render(request,'user/base_sell.html',locals())

    #return render(request, 'user/index.html')

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

            if user.pwd == password:
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                request.session['user_type'] = user.type
                type = user.type
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
        #print('in post')
        register_form = forms.RegisterForm(request.POST)
        message = '输入不合法！'
        
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            pwd1 = register_form.cleaned_data.get('password1')
            pwd2 = register_form.cleaned_data.get('password2')
            type = register_form.cleaned_data.get('type')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')
            birth = register_form.cleaned_data.get('birth')
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
                #new_user.pwd = hash_code(pwd1)
                new_user.pwd = pwd1
                new_user.email = email
                new_user.sex = sex
                new_user.type = type
                new_user.phoneNumber = phoneNumber
                new_user.birth = birth
                new_user.save()
                return redirect('/login/')
        #注册表无效
        else:
            return render(request,'user/register.html',locals())

    register_form = forms.RegisterForm()
    return render(request, 'user/register.html',locals())


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

def upload(request):
    #未登录无法上传
    if not request.session.get('is_login',None):
        #print('1 upload session')
        return redirect('/index/')
    
    if request.method == 'POST':
        form = forms.Upload(request.POST, request.FILES)
        # 将数据保存到数据库
        if form.is_valid():
            newgoods = form.save(commit=False)
            seller = models.User.objects.get(pk=request.session.get('user_id'))
            newgoods.seller_id = request.session.get('user_id')
            newgoods.save()
            #messages.success(request, "上传成功")
            print('here!!')
            return redirect('/index/')
        else:
            print(form.errors.get_json_data())
            #messages.success(request, "上传失败")
            return redirect('/upload/')
    form = forms.Upload()
    return render(request, 'user/uploadgoods.html', locals())

def sell_record(request):
    return render(request, 'user/sell_record.html', locals())

def buy_record(request):
    if not request.session.get('is_login',None):
        return redirect('/login/')
    buy_records = models.deal.objects.filter(buyer_id=request.session.get('user_id'))
    return render(request, 'user/buy_record.html', locals())

def cart(request):
    if not request.session.get('is_login',None):
        return redirect('/login/')
    carts = models.cart.objects.filter(user_id=request.session.get('user_id'))
    return render(request, 'user/cart.html', locals())

def changeInfo(request):
    #未登录 返回登陆界面
    if not request.session.get('is_login', None):
        return redirect('/login/')
    #print(1)

    if request.method == 'POST':
        form = forms.InfoForm(request.POST)
        message = '输入不合法！'

        if form.is_valid():
            username = form.cleaned_data.get('username')
            pwd1 = form.cleaned_data.get('password1')
            pwd2 = form.cleaned_data.get('password2')
            email = form.cleaned_data.get('email')
            birth = form.cleaned_data.get('birth')
            phoneNumber = form.cleaned_data.get('phoneNumber')
            # 检测输入密码是否一致
            if pwd1!=pwd2:
                message = '两次密码不同'
                return render(request,'user/changeInfo.html',locals())
            elif len(pwd1) == 0:
                message = '密码不能为空！'
                return redirect('/changeInfo/')
            elif not judge_Monile_phone(phoneNumber):
                message = '手机号格式错误！'
                return render('/changeInfo/')
            else:
                now_user = set(models.User.objects.filter(pk=request.session['user_id']))
                same_user = set(models.User.objects.filter(name=username))-now_user

                if same_user:
                    message = '用户名已存在！'
                    return render(request, 'user/changeInfo.html', locals())
                same_email = set(models.User.objects.filter(email=email))-now_user
                if same_email:
                    message = '邮箱已存在！'
                    return render(request,'user/changeInfo.html',locals())
                #print('change here!!!!!!')

                new_user = models.User.objects.filter(pk=request.session['user_id'])[0]
                #print('new_user!!!!!!!!',new_user)
                new_user.name = username
                new_user.pwd = hash_code(pwd1)
                new_user.email = email
                new_user.phoneNumber = phoneNumber
                new_user.birth = birth
                new_user.save()
                request.session['user_name'] = username
                #修改成功
                return redirect('/index/')
        # 注册表无效
        else:
            message = '输入不合法！'
            print('invalid')
            return render(request, 'user/changeInfo.html', locals())
    else:
        ids = request.session['user_id']
        now_user = models.User.objects.get(id=ids)
        dic = {'username':now_user.name,'email':now_user.email,'phoneNumber':now_user.phoneNumber,'birth':now_user.birth,
               'password1':now_user.pwd,'password2':now_user.pwd}
        
        form = forms.InfoForm(initial=dic)
        return render(request, 'user/changeInfo.html', locals())
    
def goodsInfo(request,id):
    goods = models.Goods.objects.get(id=id)
    return render(request,'goods/goodsInfo.html',locals())

@csrf_exempt
def buy_goods(request):
    if request.method == 'POST':
        goods_id = request.POST.get('goods_id')
        #print('goods_id',goods_id)
        seller_id = request.POST.get('seller_id')
        goods = models.Goods.objects.get(id=goods_id)
        price = goods.price
        # 已售出
        if goods.state == 1:
            #print('已售出')
            return JsonResponse({'status': 200, 'message': '商品已出售'})
        else:
            buy = models.User.objects.get(id=request.session['user_id'])
            # 创建交易记录
            new_deal = models.deal.objects.create(
                buyer_id=buy.id,
                seller_id=seller_id,
                goods_id=goods_id,
                date=timezone.now(),
                price=price,
            )
            new_deal.save()
            goods.state = 1 #修改商品售出状态
            goods.save()
            return JsonResponse({'status': 200, 'message': '购买成功'})
    return JsonResponse({'status': 200, 'message': '购买失败'})

def return_goods(request):
    #print('here!!!!')
    if not request.session.get('is_login',None):
        return redirect('/login/')
    if request.method == "POST":
        record_id = request.POST.get('record_id')
        record = models.deal.objects.get(id=record_id)
        goods = record.goods
        goods.state = 0 #更改为未售
        goods.save()
        record.delete()
        #print('成功删除！！！')
        return redirect('/buy_record/')
    return redirect('/buy_record/')

def cart_goods(request):
    if not request.session.get('is_login',None):
        return redirect('/login/')
    if request.method == "POST":
        goods_id = request.POST.get('goods_id')
        goods = models.Goods.objects.get(id=goods_id)
        user_id = request.session.get('user_id')
        res = models.cart.objects.filter(user_id=user_id,goods_id=goods_id)
        if res:
            messages.add_message(request, messages.INFO, '商品已在购物车中')
            return render(request, 'goods/goodsInfo.html', locals())
        else:
            
            models.cart.objects.create(
                date=timezone.now(),
                goods_id=goods_id,
                user_id=user_id
            )
            messages.add_message(request, messages.INFO, '添加成功！')
            return render(request,'goods/goodsInfo.html',locals())
   # messages.add_message(request, messages.INFO, '添加失败！')
    return render(request,'goods/goodsInfo.html',locals())

def return_cart(request):
    if not request.session.get('is_login',None):
        return redirect('/login/')
    if request.method == "POST":
        cart_id = request.POST.get('cart_id')
        cart_item = models.cart.objects.get(id=cart_id)
        
        cart_item.delete()
        #print('成功删除！！！')
        return redirect('/cart/')
    return redirect('/cart/')
    
    
        
        
        
        
    
    

        
    
    






