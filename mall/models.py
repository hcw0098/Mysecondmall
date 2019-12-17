import uuid

from django.db import models

# Create your models here.
#superuser: huang hcw1998HCW


class User(models.Model):
    #ids = models.AutoField(primary_key=True,default=0)
    gender = (
        ('male','男'),
        ('female','女'),
    )
    name = models.CharField(max_length=128,unique=True)
    pwd = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32,choices=gender,default='male')
    c_time = models.DateTimeField(auto_now_add=True)
    iden = (
        (0,'买家'),
        (1,'卖家'),
    )
    type = models.SmallIntegerField(verbose_name='身份',choices=iden,default=0)
    phoneNumber = models.CharField(max_length=11,verbose_name='手机号码',default='')

    
    def __str__(self):
        return self.name
    

    class Meta:
        ordering = ['-c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'

#商品

class Good(models.Model):
    #ids = models.AutoField(primary_key=True,default=0)
    name = models.CharField(max_length=128)
    seller = models.ForeignKey('User',on_delete=models.CASCADE,blank=True) #级联删除
    price = models.FloatField(default=0,null=False)
    #img = models.ImageField(upload_to='goods_img')
    #descrip = models.TextField()##to do

    stats = ((0,'未售'),(1,'已售'),)
    state = models.SmallIntegerField(choices=stats,default=0)
    types = (
        (0,'服装'),
        (1,'电子产品'),
        (2,'书籍'),
    )
    type = models.SmallIntegerField(choices=types, default=0)


"""
# 评论 买方和货物的关系
class Comments(models.Model):
    user = models.ForeignKey('User',on_delete=models.CASCADE)
    goods = models.ForeignKey('Goods',on_delete=models.CASCADE)
    content = models.TextField()##to do
    date = models.DateField()

#购物车，买方与货物的所属关系
class Cart(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    goods = models.ForeignKey('Goods', on_delete=models.CASCADE)
    date = models.DateField()

#卖方对商品的所属关系
class seller_have(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    goods = models.ForeignKey('Goods', on_delete=models.CASCADE)
    date = models.DateField()

#买方对商品的所属关系
class buyer_have(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    goods = models.ForeignKey('Goods', on_delete=models.CASCADE)
    date = models.DateField()

#交易记录
class deal(models.Model):
    buyer = models.ForeignKey('User', on_delete=models.CASCADE)
    seller = models.ForeignKey('User', on_delete=models.CASCADE)
    goods = models.ForeignKey('Goods', on_delete=models.CASCADE)
    date = models.DateField()
    price = models.FloatField(default=0, null=False)





"""


class Article(models.Model):
    #ids = models.AutoField(primary_key=True, default=0)
    myfile = models.ImageField(upload_to="test")



