# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0006_auto_20181020_1045'),
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('student', models.ForeignKey(to='crm.Student')),
                ('user', models.ForeignKey(to='crm.UserInfos')),
            ],
        ),
        migrations.DeleteModel(
            name='Test',
        ),
    ]
