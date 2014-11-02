# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recom', '0002_auto_20141102_0907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='appid',
            field=models.CharField(max_length=20),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='app',
            name='genres',
            field=models.CharField(default=b'[]', max_length=200),
            preserve_default=True,
        ),
    ]
