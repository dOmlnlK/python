# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_role_menus'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractTemplate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('content', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentRecoed',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('payment_type', models.SmallIntegerField(default=0, choices=[(0, '报名费'), (1, '学费'), (2, '退费')])),
                ('amount', models.IntegerField(default=500, verbose_name='费用')),
                ('date', models.DateField(auto_now_add=True)),
                ('consultant', models.ForeignKey(to='crm.UserInfos')),
            ],
        ),
        migrations.CreateModel(
            name='StudentEnrollment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('contract_argeed', models.BooleanField(default=False)),
                ('contract_argeed_date', models.DateField(verbose_name='客户同意时间', null=True, blank=True)),
                ('contract_approved', models.BooleanField(default=False)),
                ('contract_approved_date', models.DateField(verbose_name='审核通过时间', null=True, blank=True)),
                ('class_grade', models.ForeignKey(to='crm.ClassList')),
                ('consultant', models.ForeignKey(to='crm.UserInfos')),
                ('customer', models.ForeignKey(to='crm.CustomerInfos')),
            ],
        ),
        migrations.AlterField(
            model_name='student',
            name='customer',
            field=models.OneToOneField(to='crm.CustomerInfos'),
        ),
        migrations.AddField(
            model_name='paymentrecoed',
            name='enrollment',
            field=models.ForeignKey(to='crm.StudentEnrollment'),
        ),
        migrations.AddField(
            model_name='classlist',
            name='contract_template',
            field=models.ForeignKey(to='crm.ContractTemplate', null=True, blank=True),
        ),
    ]
