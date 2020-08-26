# Generated by Django 2.2.14 on 2020-08-26 15:04

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0022_deal_cached_has_no_known_investor'),
    ]

    operations = [
        migrations.AddField(
            model_name='deal',
            name='current_intention_of_investment',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100, verbose_name='Nature of the deal'), blank=True, choices=[('Agriculture', (('BIOFUELS', 'Biofuels'), ('FOOD_CROPS', 'Food crops'), ('FODDER', 'Fodder'), ('LIVESTOCK', 'Livestock'), ('NON_FOOD_AGRICULTURE', 'Non-food agricultural commodities'), ('AGRICULTURE_UNSPECIFIED', 'Agriculture unspecified'))), ('Forestry', (('TIMBER_PLANTATION', 'Timber plantation'), ('FOREST_LOGGING', 'Forest logging / management'), ('CARBON', 'For carbon sequestration/REDD'), ('FORESTRY_UNSPECIFIED', 'Forestry unspecified'))), ('Other', (('MINING', 'Mining'), ('OIL_GAS_EXTRACTION', 'Oil / Gas extraction'), ('TOURISM', 'Tourism'), ('INDUSTRY', 'Industry'), ('CONVERSATION', 'Conservation'), ('LAND_SPECULATION', 'Land speculation'), ('RENEWABLE_ENERGY', 'Renewable Energy'), ('OTHER', 'Other')))], null=True, size=None),
        ),
        migrations.AddField(
            model_name='deal',
            name='initiation_date',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='deal',
            name='transnational',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='investorventureinvolvement',
            name='investment_type',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100, verbose_name='Investment type'), blank=True, choices=[('EQUITY', 'Shares/Equity'), ('DEBT_FINANCING', 'Debt financing')], null=True, size=None),
        ),
    ]
