# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0085_switch_investor_activity_involvement_rel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investoractivityinvolvement',
            name='fk_activity',
            field=models.ForeignKey(to='landmatrix.Activity', verbose_name='Activity'),
        ),
    ]
