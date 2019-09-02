# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-06-24 07:04
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190624_0542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='uuid',
            field=models.CharField(default=uuid.UUID('2c5c76a5-e924-43f1-947b-72a277868436'), max_length=50, verbose_name='唯一标识符'),
        ),
    ]