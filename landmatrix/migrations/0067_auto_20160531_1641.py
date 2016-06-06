# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0066_auto_20160528_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='activityattributegroup',
            name='polygon',
            field=django.contrib.gis.db.models.fields.PolygonField(null=True, blank=True, srid=4326),
        ),
        migrations.AddField(
            model_name='historicalactivityattributegroup',
            name='polygon',
            field=django.contrib.gis.db.models.fields.PolygonField(null=True, blank=True, srid=4326),
        ),
        migrations.AlterField(
            model_name='filtercondition',
            name='operator',
            field=models.CharField(choices=[('not_in', 'not_in'), ('is_empty', 'is_empty'), ('gte', 'gte'), ('lte', 'lte'), ('gt', 'gt'), ('in', 'in'), ('lt', 'lt'), ('is', 'is'), ('contains', 'contains')], verbose_name='Operator', max_length=10),
        ),
        migrations.AlterField(
            model_name='publicinterfacecache',
            name='implementation_status',
            field=models.CharField(verbose_name='Implementation status', blank=True, choices=[('---------', '---------'), ('Project not started', 'Project not started'), ('Startup phase (no production)', 'Startup phase (no production)'), ('In operation (production)', 'In operation (production)'), ('Project abandoned', 'Project abandoned')], null=True, db_index=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='publicinterfacecache',
            name='negotiation_status',
            field=models.CharField(verbose_name='Negotiation status', blank=True, choices=[('---------', '---------'), ('Expression of interest', 'Expression of interest'), ('Under negotiation', 'Under negotiation'), ('Memorandum of understanding', 'Memorandum of understanding'), ('Oral Agreement', 'Oral Agreement'), ('Contract signed', 'Contract signed'), ('Negotiations failed', 'Negotiations failed'), ('Contract canceled', 'Contract canceled'), ('Contract expired', 'Contract expired'), ('Change of ownership', 'Change of ownership')], null=True, db_index=True, max_length=64),
        ),
    ]
