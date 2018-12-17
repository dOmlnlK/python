# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_auto_20181009_2005'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='menus',
            field=models.ManyToManyField(to='crm.Menus'),
        ),
    ]
