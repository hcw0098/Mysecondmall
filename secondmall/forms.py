from django import forms
from captcha.fields import CaptchaField
from .models import *

from django.utils import timezone
class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Username", 'autofocus': ''}))
    password = forms.CharField(label="密码", max_length=256,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Password"}))
    captcha = CaptchaField(label='验证码')
    

class RegisterForm(forms.Form):
    gender = (
        ('male','男'),
        ('female','女'),
    )
    iden = (
        (0, '买家'),
        (1, '卖家'),
    )
    username = forms.CharField(label='用户名',max_length=128,widget=forms.TextInput(
        attrs={'class':'form-control','placeholder': "Username"}
    ))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Password'}))
    password2 = forms.CharField(label="确认密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Password'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'Email'}))
    sex = forms.ChoiceField(label='性别', choices=gender)
    type = forms.ChoiceField(label='用户身份',choices=iden)
    captcha = CaptchaField(label='验证码')
    phoneNumber = forms.CharField(label='电话号码',max_length=11,widget=forms.TextInput(
        attrs={'class':'form-control','placeholder': "PhoneNumber"}
    ))
    years = tuple([str(x) for x in range(1900,2020)])
    birth = forms.DateField(label='出生日期',widget=forms.SelectDateWidget(years=years))## todo

class InfoForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Username"}
    ))
    password1 = forms.CharField(label="密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(label="密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    email = forms.EmailField(label="邮箱地址",
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))

    phoneNumber = forms.CharField(label='电话号码', max_length=11, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "PhoneNumber"}
    ))
    years = tuple([str(x) for x in range(1900, 2020)])
    birth = forms.DateField(label='出生日期', widget=forms.SelectDateWidget(years=years))  ## todo

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = "__all__"
        error_messages = {
            'myfile': {
                'invalid_image': '请上传正确格式的图片！'
            }
        }

class Upload(forms.ModelForm):
    class Meta:
        model = Goods
        fields = "__all__"
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control','placeholder': "Name"}),
            'price':forms.NumberInput(attrs={'class':'form-control'}),
            'type':forms.Select(attrs={'class':'form-control'}),
            'state':forms.Select(attrs={'class':'form-control'}),
            'descrip':forms.Textarea(attrs={'class':'form-control'}),
        }
        labels = {
            "name": "商品名称",
            'price':'价格',
            'type':'商品类型',
            'state':'出售状态',
            'img':'商品图片',
            'descrip':'商品描述300字',

        }

class UploadForm(forms.Form):
    pass


