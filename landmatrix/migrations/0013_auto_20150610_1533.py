# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0012_auto_20150608_1841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='high_income',
            field=models.BooleanField(verbose_name='High income', default=False),
            preserve_default=True,
        ),
    ]
