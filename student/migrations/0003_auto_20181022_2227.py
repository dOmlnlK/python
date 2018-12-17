# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_auto_20181021_1455'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='student',
        ),
        migrations.RemoveField(
            model_name='account',
            name='user',
        ),
        migrations.DeleteModel(
            name='Account',
        ),
    ]
