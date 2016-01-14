# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0026_auto_20151130_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investorventureinvolvement',
            name='fk_investor',
            field=models.ForeignKey(to='landmatrix.Investor', related_name='+'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='investorventureinvolvement',
            name='fk_venture',
            field=models.ForeignKey(to='landmatrix.Investor', related_name='+'),
            preserve_default=True,
        ),
    ]
