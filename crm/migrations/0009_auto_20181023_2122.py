# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0008_auto_20181022_2251'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userinfos',
            options={'permissions': (('crm_model_detail', '可以查看bestadmin每张表里所有的数据'), ('crm_model_change_view', '可以访问bestadmin表里每条数据的修改页'), ('crm_model_change', '可以对bestadmin表里的每条数据进行修改'), ('crm_model_add_view', '可以访问bestadmin每张表的数据增加页'), ('crm_model_add', '可以对bestadmin每张表进行数据添加'))},
        ),
    ]
