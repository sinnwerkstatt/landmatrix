# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0080_auto_20160625_1825'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='investoractivityinvolvement',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='investoractivityinvolvement',
            name='percentage',
        ),
    ]
