# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-06-24 05:42
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='uuid',
            field=models.CharField(default=uuid.UUID('73fcdce0-5954-4f37-933e-2e56222c58c8'), max_length=50, verbose_name='唯一标识符'),
        ),
    ]