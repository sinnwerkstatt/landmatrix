# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0023_auto_20151116_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investor',
            name='classification',
            field=models.CharField(null=True, choices=[('10', 'Private company'), ('20', 'Stock-exchange listed company'), ('30', 'Individual entrepreneur'), ('40', 'Investment fund'), ('50', 'Semi state-owned company'), ('60', 'State-/government(owned)'), ('70', 'Other (please specify in comment field)')], max_length=2, blank=True),
            preserve_default=True,
        ),
    ]
