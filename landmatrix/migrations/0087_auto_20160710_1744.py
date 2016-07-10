# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0086_reverse_investor_activity_involvement_rel'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='publicinterfacecache',
            index_together=set([]),
        ),
        migrations.RemoveField(
            model_name='publicinterfacecache',
            name='fk_activity',
        ),
        migrations.AddField(
            model_name='activity',
            name='deal_scope',
            field=models.CharField(blank=True, choices=[('domestic', 'Domestic'), ('transnational', 'Transnational')], null=True, max_length=16, db_index=True, verbose_name='Deal scope'),
        ),
        migrations.AddField(
            model_name='activity',
            name='deal_size',
            field=models.IntegerField(blank=True, null=True, db_index=True, verbose_name='Deal size'),
        ),
        migrations.AddField(
            model_name='activity',
            name='implementation_status',
            field=models.CharField(blank=True, choices=[('', '---------'), ('Project not started', 'Project not started'), ('Startup phase (no production)', 'Startup phase (no production)'), ('In operation (production)', 'In operation (production)'), ('Project abandoned', 'Project abandoned')], null=True, max_length=64, db_index=True, verbose_name='Implementation status'),
        ),
        migrations.AddField(
            model_name='activity',
            name='is_public',
            field=models.BooleanField(default=False, db_index=True, verbose_name='Is this a public deal?'),
        ),
        migrations.AddField(
            model_name='activity',
            name='negotiation_status',
            field=models.CharField(blank=True, choices=[('', '---------'), ('Expression of interest', 'Intended (Expression of interest)'), ('Under negotiation', 'Intended (Under negotiation)'), ('Memorandum of understanding', 'Intended (Memorandum of understanding)'), ('Oral agreement', 'Concluded (Oral Agreement)'), ('Contract signed', 'Concluded (Contract signed)'), ('Negotiations failed', 'Failed (Negotiations failed)'), ('Contract canceled', 'Failed (Contract canceled)'), ('Contract expired', 'Failed (Contract expired)'), ('Change of ownership', 'Change of ownership')], null=True, max_length=64, db_index=True, verbose_name='Negotiation status'),
        ),
        migrations.AlterIndexTogether(
            name='activity',
            index_together=set([('is_public', 'deal_scope'), ('is_public', 'deal_scope', 'negotiation_status'), ('is_public', 'deal_scope', 'implementation_status'), ('is_public', 'deal_scope', 'negotiation_status', 'implementation_status')]),
        ),
        migrations.DeleteModel(
            name='PublicInterfaceCache',
        ),
    ]
