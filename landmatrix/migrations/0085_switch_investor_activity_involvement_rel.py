# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0084_auto_20160701_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investoractivityinvolvement',
            name='fk_activity',
            field=models.ForeignKey(verbose_name='Activity', to='landmatrix.HistoricalActivity'),
        ),
    ]
