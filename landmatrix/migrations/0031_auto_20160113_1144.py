# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_hstore.fields
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('landmatrix', '0030_auto_20151209_1447'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalActivity',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, blank=True, auto_created=True)),
                ('activity_identifier', models.IntegerField(verbose_name='Activity identifier', db_index=True)),
                ('availability', models.FloatField(verbose_name='availability', blank=True, null=True)),
                ('fully_updated', models.DateTimeField(verbose_name='Fully updated', blank=True, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('fk_status', models.ForeignKey(related_name='+', blank=True, null=True, to='landmatrix.Status', db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING)),
                ('history_user', models.ForeignKey(related_name='+', null=True, to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
                'verbose_name': 'historical activity',
                'get_latest_by': 'history_date',
                'ordering': ('-history_date', '-history_id'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalActivityAttributeGroup',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, blank=True, auto_created=True)),
                ('date', models.DateField(verbose_name='Date', db_index=True, blank=True, null=True)),
                ('attributes', django_hstore.fields.DictionaryField(db_index=True)),
                ('name', models.CharField(max_length=255, blank=True, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('fk_activity', models.ForeignKey(related_name='+', blank=True, null=True, to='landmatrix.Activity', db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING)),
                ('fk_language', models.ForeignKey(related_name='+', blank=True, null=True, to='landmatrix.Language', db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING)),
                ('history_user', models.ForeignKey(related_name='+', null=True, to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
                'verbose_name': 'historical activity attribute group',
                'get_latest_by': 'history_date',
                'ordering': ('-history_date', '-history_id'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalInvestor',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, blank=True, auto_created=True)),
                ('investor_identifier', models.IntegerField(verbose_name='Investor id', db_index=True)),
                ('name', models.CharField(verbose_name='Name', max_length=1024)),
                ('classification', models.CharField(max_length=2, choices=[('10', 'Private company'), ('20', 'Stock-exchange listed company'), ('30', 'Individual entrepreneur'), ('40', 'Investment fund'), ('50', 'Semi state-owned company'), ('60', 'State-/government(owned)'), ('70', 'Other (please specify in comment field)')], blank=True, null=True)),
                ('comment', models.TextField(verbose_name='Comment', blank=True, null=True)),
                ('timestamp', models.DateTimeField(verbose_name='Timestamp', editable=False, blank=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('fk_country', models.ForeignKey(related_name='+', blank=True, null=True, to='landmatrix.Country', db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING)),
                ('fk_status', models.ForeignKey(related_name='+', blank=True, null=True, to='landmatrix.Status', db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING)),
                ('history_user', models.ForeignKey(related_name='+', null=True, to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
                'verbose_name': 'historical investor',
                'get_latest_by': 'history_date',
                'ordering': ('-history_date', '-history_id'),
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='investor',
            name='version',
        ),
        migrations.AlterUniqueTogether(
            name='activity',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='activity',
            name='version',
        ),
    ]
