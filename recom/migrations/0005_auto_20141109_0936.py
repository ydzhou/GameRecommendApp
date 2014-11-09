# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recom', '0004_auto_20141109_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='recom_apps',
            field=models.TextField(default=b'[-1]'),
            preserve_default=True,
        ),
    ]
