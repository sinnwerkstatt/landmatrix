# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0038_auto_20160310_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='browsecondition',
            name='value',
            field=models.CharField(verbose_name='Value', max_length=1024),
        ),
    ]
