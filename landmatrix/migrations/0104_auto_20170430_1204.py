# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0103_auto_20170427_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investorventureinvolvement',
            name='fk_status',
            field=models.ForeignKey(to='landmatrix.Status', verbose_name='Status', default=1),
        ),
    ]
