# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0071_ordered_filter_operator_choices'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activityattribute',
            name='date',
            field=models.CharField(blank=True, null=True, verbose_name='Year or Date', db_index=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='activityattribute',
            name='fk_activity',
            field=models.ForeignKey(to='landmatrix.Activity', verbose_name='Activity', related_name='attributes'),
        ),
        migrations.AlterField(
            model_name='activityattribute',
            name='fk_group',
            field=models.ForeignKey(blank=True, null=True, to='landmatrix.ActivityAttributeGroup', verbose_name='Activity Attribute Group', related_name='attributes'),
        ),
        migrations.AlterField(
            model_name='historicalactivityattribute',
            name='date',
            field=models.CharField(blank=True, null=True, verbose_name='Year or Date', db_index=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='publicinterfacecache',
            name='negotiation_status',
            field=models.CharField(blank=True, null=True, db_index=True, verbose_name='Negotiation status', choices=[('---------', '---------'), ('Intended (Expression of interest)', 'Intended (Expression of interest)'), ('Intended (Under negotiation)', 'Intended (Under negotiation)'), ('Intended (Memorandum of understanding)', 'Intended (Memorandum of understanding)'), ('Concluded (Oral Agreement)', 'Concluded (Oral Agreement)'), ('Concluded (Contract signed)', 'Concluded (Contract signed)'), ('Failed (Negotiations failed)', 'Failed (Negotiations failed)'), ('Failed (Contract canceled)', 'Failed (Contract canceled)'), ('Failed (Contract expired)', 'Failed (Contract expired)'), ('Change of ownership', 'Change of ownership')], max_length=64),
        ),
    ]
