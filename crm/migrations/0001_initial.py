# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(unique=True, max_length=32)),
                ('addr', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='ClassList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('semester', models.PositiveSmallIntegerField(verbose_name='学期')),
                ('start_date', models.DateField(verbose_name='开学时间')),
                ('graduate_date', models.DateField(blank=True, verbose_name='毕业时间', null=True)),
                ('class_type', models.SmallIntegerField(default=0, choices=[(0, '脱产班'), (1, '周末班'), (2, '网络班')])),
                ('branch', models.ForeignKey(to='crm.Branch')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='课程名称', unique=True, max_length=32)),
                ('outline', models.TextField(verbose_name='课程大纲')),
                ('price', models.PositiveSmallIntegerField(verbose_name='课程价格')),
                ('period', models.PositiveSmallIntegerField(default=5, verbose_name='课程周期(月)')),
            ],
        ),
        migrations.CreateModel(
            name='CourseRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('day_num', models.PositiveSmallIntegerField(verbose_name='课程节次')),
                ('title', models.CharField(verbose_name='本节主题', max_length=32)),
                ('content', models.TextField(verbose_name='本节内容')),
                ('has_homework', models.BooleanField(default=True, verbose_name='本节是否有作业')),
                ('homework', models.TextField(blank=True, verbose_name='作业需求', null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('class_grade', models.ForeignKey(verbose_name='上课班级', to='crm.ClassList')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerFollowUp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('content', models.TextField(verbose_name='跟进内容')),
                ('status', models.SmallIntegerField(choices=[(0, '近期无报名计划'), (1, '1个月内报名'), (2, '两周内报名'), (3, '已经报名')])),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerInfos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(default=None, max_length=32)),
                ('contact_type', models.SmallIntegerField(default=0, choices=[(0, 'qq'), (1, '微信'), (2, '手机')])),
                ('contact', models.CharField(unique=True, max_length=64)),
                ('consult_content', models.TextField(verbose_name='咨询内容')),
                ('status', models.SmallIntegerField(choices=[(0, '未报名'), (1, '已报名'), (2, '已退学')])),
                ('source', models.SmallIntegerField(choices=[(0, 'QQ群'), (1, '51CTO'), (2, '百度推广'), (3, '知乎'), (4, '转介绍'), (5, '其他')])),
                ('date', models.DateField(auto_now_add=True)),
                ('consult_courses', models.ManyToManyField(verbose_name='咨询课程', to='crm.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='角色', max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('class_grades', models.ManyToManyField(to='crm.ClassList')),
                ('customer', models.ForeignKey(to='crm.CustomerInfos')),
            ],
        ),
        migrations.CreateModel(
            name='StudyRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('score', models.SmallIntegerField(choices=[(90, 'A'), (80, 'B'), (60, 'C'), (40, 'D'), (0, 'N/A'), (-1, 'COPY')])),
                ('show_status', models.SmallIntegerField(default=1, choices=[(0, '缺勤'), (1, '已签到'), (2, '迟到'), (3, '早退')])),
                ('note', models.TextField(blank=True, verbose_name='成绩备注', null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('course_record', models.ForeignKey(to='crm.CourseRecord')),
                ('student', models.ForeignKey(to='crm.Student')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='名字', max_length=32)),
                ('role', models.ManyToManyField(to='crm.Role')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='customerinfos',
            name='consultant',
            field=models.ForeignKey(verbose_name='咨询顾问', to='crm.UserInfos'),
        ),
        migrations.AddField(
            model_name='customerinfos',
            name='referral_from',
            field=models.ForeignKey(null=True, to='crm.CustomerInfos', blank=True),
        ),
        migrations.AddField(
            model_name='customerfollowup',
            name='customer',
            field=models.ForeignKey(to='crm.CustomerInfos'),
        ),
        migrations.AddField(
            model_name='customerfollowup',
            name='user',
            field=models.ForeignKey(verbose_name='跟进人', to='crm.UserInfos'),
        ),
        migrations.AddField(
            model_name='courserecord',
            name='teacher',
            field=models.ForeignKey(verbose_name='本节讲师', to='crm.UserInfos'),
        ),
        migrations.AddField(
            model_name='classlist',
            name='course',
            field=models.ForeignKey(to='crm.Course'),
        ),
        migrations.AddField(
            model_name='classlist',
            name='teachers',
            field=models.ManyToManyField(verbose_name='讲师', to='crm.UserInfos'),
        ),
        migrations.AlterUniqueTogether(
            name='courserecord',
            unique_together=set([('class_grade', 'day_num')]),
        ),
        migrations.AlterUniqueTogether(
            name='classlist',
            unique_together=set([('course', 'semester', 'branch', 'class_type')]),
        ),
    ]
