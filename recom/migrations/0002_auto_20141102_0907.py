# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recom', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='app',
            old_name='app_id',
            new_name='appid',
        ),
        migrations.AddField(
            model_name='app',
            name='publisher',
            field=models.CharField(default=b'NA', max_length=100),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='app',
            name='release_date',
            field=models.CharField(default=b'NA', max_length=50),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='app',
            name='url',
            field=models.TextField(default=b'NA'),
            preserve_default=True,
        ),
    ]
