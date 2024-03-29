# Generated by Django 3.0 on 2019-12-17 20:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('myfile', models.ImageField(upload_to='test')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('pwd', models.CharField(max_length=256)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('sex', models.CharField(choices=[('male', '男'), ('female', '女')], default='male', max_length=32)),
                ('c_time', models.DateTimeField(auto_now_add=True)),
                ('type', models.SmallIntegerField(choices=[(0, '买家'), (1, '卖家')], default=0, verbose_name='身份')),
                ('phoneNumber', models.CharField(default='', max_length=11, verbose_name='手机号码')),
                ('birth', models.DateField(blank=True)),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'ordering': ['-c_time'],
            },
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('price', models.FloatField(default=0)),
                ('img', models.ImageField(blank=True, upload_to='goods_img')),
                ('descrip', models.TextField(blank=True, default='', max_length=1024)),
                ('state', models.SmallIntegerField(choices=[(0, '未售'), (1, '已售')], default=0)),
                ('type', models.SmallIntegerField(choices=[(0, '服装'), (1, '电子产品'), (2, '书籍')], default=0)),
                ('seller', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='secondmall.User')),
            ],
        ),
    ]
