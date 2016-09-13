# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0088_auto_20160812_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitychangeset',
            name='timestamp',
            field=models.DateTimeField(verbose_name='Timestamp', auto_now_add=True, default=datetime.datetime(2016, 9, 13, 22, 56, 55, 904585, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
