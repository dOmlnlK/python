# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menus',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=32)),
                ('url_type', models.SmallIntegerField(default=0, choices=[(0, 'absolute'), (1, 'dynamic')])),
                ('url_name', models.CharField(max_length=128)),
            ],
        ),
        migrations.AlterField(
            model_name='userinfos',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='menus',
            unique_together=set([('name', 'url_name')]),
        ),
    ]
