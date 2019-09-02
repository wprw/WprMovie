# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-06-24 07:21
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20190624_0717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='uuid',
            field=models.CharField(default=uuid.UUID('ee291b82-f0b7-41c5-9bb0-b4f000c74445'), max_length=50, verbose_name='唯一标识符'),
        ),
    ]