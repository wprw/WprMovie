# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-07-26 05:17
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20190711_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='uuid',
            field=models.CharField(default=uuid.UUID('89056c81-0343-4d27-b999-3ab97425ca15'), max_length=50, verbose_name='唯一标识符'),
        ),
    ]