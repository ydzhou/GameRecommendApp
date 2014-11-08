# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recom', '0002_auto_20141107_0852'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='friend',
            field=models.ManyToManyField(related_name='friend_rel_+', to='recom.User'),
            preserve_default=True,
        ),
    ]
