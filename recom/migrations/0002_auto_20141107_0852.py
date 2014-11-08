# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recom', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userownedgames',
            name='app',
        ),
        migrations.AddField(
            model_name='userownedgames',
            name='appid',
            field=models.CharField(default=b'', max_length=20),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='last_update',
            field=models.DateField(default=None),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userownedgames',
            name='playtime',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userownedgames',
            name='playtime_2weeks',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
