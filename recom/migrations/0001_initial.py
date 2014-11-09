# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('appid', models.CharField(max_length=20)),
                ('name', models.CharField(default=b'NA', max_length=100)),
                ('descript', models.TextField(default=b'NA')),
                ('img', models.TextField(default=b'NA')),
                ('score', models.IntegerField(default=0)),
                ('genres', models.TextField(default=b'{success:False}')),
                ('publisher', models.CharField(default=b'NA', max_length=100)),
                ('release_date', models.CharField(default=b'NA', max_length=50)),
                ('url', models.TextField(default=b'NA')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('steam_id', models.CharField(max_length=17)),
                ('visited', models.IntegerField(default=0)),
                ('friend', models.ManyToManyField(related_name='friend_rel_+', to='recom.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserOwnedGames',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('appid', models.CharField(default=b'', max_length=20)),
                ('playtime', models.IntegerField(default=0)),
                ('playtime_2weeks', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to='recom.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
