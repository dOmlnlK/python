# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('crm', '0007_auto_20181022_2227'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfos',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(blank=True, verbose_name='last login', null=True)),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status', default=False)),
                ('email', models.EmailField(unique=True, verbose_name='email address', max_length=255)),
                ('name', models.CharField(verbose_name='姓名', max_length=64)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', blank=True, to='auth.Group', verbose_name='groups', related_query_name='user', related_name='user_set')),
                ('role', models.ManyToManyField(blank=True, to='crm.Role', null=True)),
                ('user_permissions', models.ManyToManyField(help_text='Specific permissions for this user.', blank=True, to='auth.Permission', verbose_name='user permissions', related_query_name='user', related_name='user_set')),
            ],
            options={
                'permissions': (('crm_model_all', '可以查看bestadmin每张表里所有的数据'), ('crm_model_change_view', '可以访问bestadmin表里每条数据的修改页'), ('crm_model_change', '可以对bestadmin表里的每条数据进行修改'), ('crm_model_add_view', '可以访问bestadmin每张表的数据增加页'), ('crm_model_add', '可以对bestadmin每张表进行数据添加')),
            },
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='role',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user_permissions',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
