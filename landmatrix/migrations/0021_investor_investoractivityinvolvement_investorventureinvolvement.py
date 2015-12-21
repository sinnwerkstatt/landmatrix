# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import landmatrix.models.default_string_representation
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0020_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Investor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('investor_identifier', models.IntegerField(verbose_name='Investor id', db_index=True)),
                ('name', models.CharField(max_length=1024, verbose_name='Name')),
                ('classification', models.CharField(max_length=2, choices=[('10', 'Private company'), ('20', 'Stock-exchange listed company'), ('30', 'Individual entrepreneur'), ('40', 'Investment fund'), ('50', 'Semi state-owned company'), ('60', 'State-/government(owned)'), ('70', 'Other (please specify in comment field)')])),
                ('comment', models.TextField(verbose_name='Comment')),
                ('timestamp', models.DateTimeField(verbose_name='Timestamp', auto_now_add=True)),
                ('version', models.IntegerField(verbose_name='Version', db_index=True)),
                ('country', models.ForeignKey(blank=True, null=True, verbose_name='Country', to='landmatrix.Country')),
                ('fk_status', models.ForeignKey(verbose_name='Status', to='landmatrix.Status')),
            ],
            options={
            },
            bases=(landmatrix.models.default_string_representation.DefaultStringRepresentation, models.Model),
        ),
        migrations.CreateModel(
            name='InvestorActivityInvolvement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('percentage', models.FloatField(blank=True, verbose_name='Percentage', validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)], null=True)),
                ('timestamp', models.DateTimeField(verbose_name='Timestamp', auto_now_add=True)),
                ('activity', models.ForeignKey(verbose_name='Activity', to='landmatrix.Activity')),
                ('fk_status', models.ForeignKey(verbose_name='Status', to='landmatrix.Status')),
                ('investor', models.ForeignKey(verbose_name='Investor', to='landmatrix.Investor')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InvestorVentureInvolvement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('percentage', models.FloatField(blank=True, verbose_name='Percentage', validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)], null=True)),
                ('role', models.CharField(max_length=2, choices=[('ST', 'Stakeholder'), ('IN', 'Investor')])),
                ('timestamp', models.DateTimeField(verbose_name='Timestamp', auto_now_add=True)),
                ('fk_status', models.ForeignKey(verbose_name='Status', to='landmatrix.Status')),
                ('investor', models.ForeignKey(related_name='+', verbose_name='Investor', to='landmatrix.InvestorVentureInvolvement')),
                ('venture', models.ForeignKey(related_name='+', verbose_name='Venture', to='landmatrix.InvestorVentureInvolvement')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
