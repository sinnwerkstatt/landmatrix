# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0006_status_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='fk_status',
            field=models.ForeignKey(verbose_name='Status', to='landmatrix.Status', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='primaryinvestor',
            name='fk_status',
            field=models.ForeignKey(verbose_name='Status', to='landmatrix.Status', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stakeholder',
            name='fk_status',
            field=models.ForeignKey(verbose_name='status', to='landmatrix.Status', default=1),
            preserve_default=False,
        ),
    ]
