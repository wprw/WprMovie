# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-07-27 09:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0008_auto_20190727_0826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='play_id',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='电影ID'),
        ),
    ]
