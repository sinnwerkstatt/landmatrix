# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import landmatrix.models.default_string_representation


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0027_auto_20151130_1325'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicInterfaceCache',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('is_deal', models.BooleanField(default=False, db_index=True, verbose_name='Is this a deal?')),
                ('deal_scope', models.CharField(db_index=True, max_length=16, choices=[('domestic', 'domestic'), ('transnational', 'transnational')], verbose_name='Deal scope')),
                ('negotiation_status', models.CharField(db_index=True, max_length=64, choices=[('Intended (Expression of interest)', 'Intended (Expression of interest)'), ('Intended (Under negotiation)', 'Intended (Under negotiation)'), ('Concluded (Oral Agreement)', 'Concluded (Oral Agreement)'), ('Concluded (Contract signed)', 'Concluded (Contract signed)'), ('Failed (Negotiations failed)', 'Failed (Negotiations failed)'), ('Failed (Contract canceled)', 'Failed (Contract canceled)')], verbose_name='Negotiation status')),
                ('implementation_status', models.CharField(db_index=True, max_length=64, choices=[('Project not started', 'Project not started'), ('Startup phase (no production)', 'Startup phase (no production)'), ('In operation (production)', 'In operation (production)'), ('Project abandoned', 'Project abandoned')], verbose_name='Implementation status')),
                ('deal_size', models.IntegerField(db_index=True, verbose_name='Deal size')),
                ('fk_activity', models.ForeignKey(to='landmatrix.Activity', verbose_name='Activity')),
            ],
            options={
            },
            bases=(landmatrix.models.default_string_representation.DefaultStringRepresentation, models.Model),
        ),
        migrations.AlterIndexTogether(
            name='publicinterfacecache',
            index_together=set([('is_deal', 'deal_scope'), ('is_deal', 'deal_scope', 'implementation_status'), ('is_deal', 'deal_scope', 'negotiation_status'), ('is_deal', 'deal_scope', 'negotiation_status', 'implementation_status')]),
        ),
    ]
