# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-06-24 07:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='length',
            field=models.CharField(max_length=255, verbose_name='时长'),
        ),
    ]
