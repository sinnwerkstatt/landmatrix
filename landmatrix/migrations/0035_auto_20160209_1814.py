# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0034_auto_20160204_1654'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activitychangeset',
            name='source',
        ),
        migrations.AlterField(
            model_name='activitychangeset',
            name='fk_activity',
            field=models.ForeignKey(null=True, to='landmatrix.Activity', verbose_name='Activity', blank=True),
        ),
    ]
