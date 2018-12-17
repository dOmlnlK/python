# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0009_auto_20181023_2122'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userinfos',
            options={'permissions': (('crm_model_detail', '可以查看bestadmin每张表里所有的数据'), ('crm_model_change', '可以对bestadmin表里的每条数据进行修改'), ('crm_model_add', '可以对bestadmin每张表进行数据添加'))},
        ),
    ]
