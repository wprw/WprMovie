# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-07-11 15:24
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20190624_0721'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='imagecontent',
            field=models.FileField(default=2, upload_to='faceimg/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='uuid',
            field=models.CharField(default=uuid.UUID('6a2668c7-bdbc-4161-a848-8752a0ce910a'), max_length=50, verbose_name='唯一标识符'),
        ),
    ]
