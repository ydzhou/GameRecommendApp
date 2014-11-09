# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recom', '0002_auto_20141109_0446'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='visited',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='recom_apps',
            field=models.CharField(default=b'[False]', max_length=200),
            preserve_default=True,
        ),
    ]
