"""login URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
##app
from secondmall import views

from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from login.settings import MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('', views.index),
    url(r'^media/(?P<path>.*)$', serve, {"document_root":MEDIA_ROOT}),
    path('login/', views.login),
    path('register/', views.register),
    path('logout/', views.logout),
    path('captcha/', include('captcha.urls')),
    path('test/', views.UploadGoodsView.as_view()),
    path('upload/',views.upload),
    path('sell_record/', views.sell_record),
    path('buy_record/', views.buy_record),
    path('cart/', views.cart),
    path('changeInfo/', views.changeInfo),
    url(r'^goodsInfo/(\d+)/$', views.goodsInfo,name='goodsInfo'),
    path('buy_goods/', views.buy_goods),
    path('return_goods/', views.return_goods),
    path('cart_goods/',views.cart_goods),
    path('return_carts/',views.return_cart)
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

