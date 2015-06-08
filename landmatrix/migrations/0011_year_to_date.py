# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0010_language'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activityattributegroup',
            name='year',
        ),
        migrations.AddField(
            model_name='activityattributegroup',
            name='date',
            field=models.DateField(verbose_name='Date', blank=True, db_index=True, null=True),
        ),
    ]
