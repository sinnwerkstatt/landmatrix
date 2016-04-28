# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0055_auto_20160418_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filtercondition',
            name='operator',
            field=models.CharField(verbose_name='Operator', max_length=10, choices=[('gte', 'gte'), ('lte', 'lte'), ('is', 'is'), ('in', 'in'), ('is_empty', 'is_empty'), ('not_in', 'not_in'), ('gt', 'gt'), ('contains', 'contains'), ('lt', 'lt')]),
        ),
        migrations.AlterField(
            model_name='publicinterfacecache',
            name='negotiation_status',
            field=models.CharField(verbose_name='Negotiation status', max_length=64, db_index=True, choices=[('---------', '---------'), ('Expression of interest', 'Expression of interest'), ('Under negotiation', 'Under negotiation'), ('Memorandum of understanding', 'Memorandum of understanding'), ('Oral Agreement', 'Oral Agreement'), ('Contract signed', 'Contract signed'), ('Negotiations failed', 'Negotiations failed'), ('Contract canceled', 'Contract canceled'), ('Contract expired', 'Contract expired'), ('Change of ownership', 'Change of ownership')], null=True, blank=True),
        ),
    ]
