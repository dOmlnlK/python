# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_auto_20181022_2227'),
        ('auth', '0006_require_contenttypes_0002'),
        ('crm', '0006_auto_20181020_1045'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(verbose_name='last login', null=True, blank=True)),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name='email address')),
                ('name', models.CharField(max_length=64, verbose_name='姓名')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(to='auth.Group', blank=True, related_query_name='user', verbose_name='groups', related_name='user_set', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.')),
                ('role', models.ManyToManyField(to='crm.Role', null=True, blank=True)),
                ('user_permissions', models.ManyToManyField(to='auth.Permission', blank=True, related_query_name='user', verbose_name='user permissions', related_name='user_set', help_text='Specific permissions for this user.')),
            ],
            options={
                'permissions': (('crm_model_all', '可以查看bestadmin每张表里所有的数据'), ('crm_model_change_view', '可以访问bestadmin表里每条数据的修改页'), ('crm_model_change', '可以对bestadmin表里的每条数据进行修改'), ('crm_model_add_view', '可以访问bestadmin每张表的数据增加页'), ('crm_model_add', '可以对bestadmin每张表进行数据添加')),
            },
        ),
        migrations.RemoveField(
            model_name='userinfos',
            name='role',
        ),
        migrations.RemoveField(
            model_name='userinfos',
            name='user',
        ),
        migrations.AlterField(
            model_name='classlist',
            name='teachers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='讲师'),
        ),
        migrations.AlterField(
            model_name='courserecord',
            name='teacher',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='本节讲师'),
        ),
        migrations.AlterField(
            model_name='customerfollowup',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='跟进人'),
        ),
        migrations.AlterField(
            model_name='customerinfos',
            name='consultant',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='咨询顾问'),
        ),
        migrations.AlterField(
            model_name='paymentrecoed',
            name='consultant',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='studentenrollment',
            name='consultant',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='UserInfos',
        ),
    ]
