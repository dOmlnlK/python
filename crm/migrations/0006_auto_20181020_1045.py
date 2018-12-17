# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0005_auto_20181019_2028'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerinfos',
            name='id_num',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='customerinfos',
            name='sex',
            field=models.SmallIntegerField(blank=True, choices=[(0, '女'), (1, '男')], null=True),
        ),
    ]
