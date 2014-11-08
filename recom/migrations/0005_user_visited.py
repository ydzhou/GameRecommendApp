# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recom', '0004_remove_user_last_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='visited',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
