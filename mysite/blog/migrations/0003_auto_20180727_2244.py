# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-07-27 14:44
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20180727_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='c_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 27, 14, 44, 53, 14261, tzinfo=utc)),
        ),
    ]