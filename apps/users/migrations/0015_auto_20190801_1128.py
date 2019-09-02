# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-08-01 11:28
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_auto_20190801_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlog',
            name='add_time',
            field=models.DateField(verbose_name='登录时间'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='uuid',
            field=models.CharField(default=uuid.UUID('f5f66f56-a26b-43a9-85b5-acc734e81235'), max_length=50, verbose_name='唯一标识符'),
        ),
    ]
