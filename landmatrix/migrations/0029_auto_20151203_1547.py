# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0028_auto_20151203_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicinterfacecache',
            name='deal_scope',
            field=models.CharField(null=True, choices=[('domestic', 'domestic'), ('transnational', 'transnational')], db_index=True, verbose_name='Deal scope', blank=True, max_length=16),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicinterfacecache',
            name='deal_size',
            field=models.IntegerField(null=True, verbose_name='Deal size', blank=True, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicinterfacecache',
            name='implementation_status',
            field=models.CharField(null=True, choices=[('Project not started', 'Project not started'), ('Startup phase (no production)', 'Startup phase (no production)'), ('In operation (production)', 'In operation (production)'), ('Project abandoned', 'Project abandoned')], db_index=True, verbose_name='Implementation status', blank=True, max_length=64),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicinterfacecache',
            name='negotiation_status',
            field=models.CharField(null=True, choices=[('Intended (Expression of interest)', 'Intended (Expression of interest)'), ('Intended (Under negotiation)', 'Intended (Under negotiation)'), ('Concluded (Oral Agreement)', 'Concluded (Oral Agreement)'), ('Concluded (Contract signed)', 'Concluded (Contract signed)'), ('Failed (Negotiations failed)', 'Failed (Negotiations failed)'), ('Failed (Contract canceled)', 'Failed (Contract canceled)')], db_index=True, verbose_name='Negotiation status', blank=True, max_length=64),
            preserve_default=True,
        ),
    ]
