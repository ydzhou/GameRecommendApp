# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recom', '0003_auto_20141109_0921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='genres',
            field=models.TextField(default=b'{success:False}'),
            preserve_default=True,
        ),
    ]
