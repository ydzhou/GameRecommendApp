# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recom', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='genres',
            field=models.CharField(default=b'{success:False}', max_length=2000),
            preserve_default=True,
        ),
    ]
