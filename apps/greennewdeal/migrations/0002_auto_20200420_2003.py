# Generated by Django 2.2.12 on 2020-04-20 18:03

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('greennewdeal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deal',
            name='current_contract_size',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='current_implementation_status',
            field=models.IntegerField(blank=True, choices=[(10, 'Project not started'), (20, 'Startup phase (no production)'), (30, 'In operation (production)'), (40, 'Project abandoned')], null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='current_negotiation_status',
            field=models.IntegerField(blank=True, choices=[(10, 'Expression of interest'), (11, 'Under negotiation'), (12, 'Memorandum of understanding'), (20, 'Oral agreement'), (21, 'Contract signed'), (30, 'Negotiations failed'), (31, 'Contract canceled'), (32, 'Contract expired'), (40, 'Change of ownership')], null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='current_production_size',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='deal_size',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='fully_updated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='deal',
            name='geojson',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='private',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='deal',
            name='private_comment',
            field=models.TextField(blank=True, verbose_name='Comment why this deal is private'),
        ),
        migrations.AddField(
            model_name='deal',
            name='private_reason',
            field=models.IntegerField(blank=True, choices=[(10, 'Temporary removal from PI after criticism'), (20, 'Research in progress'), (30, 'Land Observatory Import')], null=True),
        ),
    ]