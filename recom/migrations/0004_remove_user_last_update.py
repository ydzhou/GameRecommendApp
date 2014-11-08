# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recom', '0003_user_friend'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='last_update',
        ),
    ]
