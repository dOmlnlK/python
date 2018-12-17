# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_auto_20181018_2248'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='studentenrollment',
            unique_together=set([('customer', 'class_grade')]),
        ),
    ]
