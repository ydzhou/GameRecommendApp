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
                ('app_id', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=100)),
                ('descript', models.TextField()),
                ('img', models.TextField()),
                ('score', models.IntegerField()),
                ('genres', models.CharField(max_length=200)),
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
                ('last_update', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserOwnedGames',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('playtime', models.IntegerField()),
                ('playtime_2weeks', models.IntegerField()),
                ('app', models.ManyToManyField(to='recom.App')),
                ('user', models.ForeignKey(to='recom.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
