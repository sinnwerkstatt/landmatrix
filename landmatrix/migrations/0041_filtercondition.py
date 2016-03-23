# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0040_filterpreset'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilterCondition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('variable', models.CharField(max_length=32, choices=[('target_country', 'Target Country'), ('location', 'Location'), ('intention', 'Intention'), ('intended_size', 'Intended Size'), ('contract_size', 'Contract Size'), ('production_size', 'Production Size'), ('negotiation_status', 'Negotiation Status'), ('implementation_status', 'Implementation Status'), ('crops', 'Crops'), ('nature', 'Nature'), ('contract_farming', 'Contract Farming'), ('url', 'Url'), ('type', 'Type'), ('company', 'Company'), ('type', 'Type'), ('investor_name', 'Investor Name'), ('country', 'Country')], verbose_name='Variable')),
                ('operator', models.CharField(max_length=10, choices=[('contains', 'contains'), ('gte', 'gte'), ('not_in', 'not_in'), ('is_empty', 'is_empty'), ('gt', 'gt'), ('lt', 'lt'), ('in', 'in'), ('lte', 'lte'), ('is', 'is')], verbose_name='Operator')),
                ('value', models.CharField(max_length=1024, verbose_name='Value')),
                ('rule', models.ForeignKey(to='landmatrix.FilterPreset')),
            ],
        ),
    ]
