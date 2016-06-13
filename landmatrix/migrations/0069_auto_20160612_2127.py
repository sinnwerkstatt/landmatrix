# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.contrib.gis.db.models.fields
from django.conf import settings
import landmatrix.models.default_string_representation


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('landmatrix', '0068_auto_20160531_1728'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityAttribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255, blank=True, null=True)),
                ('value', models.TextField(max_length=255, blank=True, null=True)),
                ('date', models.DateField(db_index=True, verbose_name='Date', blank=True, null=True)),
                ('polygon', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, blank=True, null=True)),
                ('fk_activity', models.ForeignKey(to='landmatrix.Activity', verbose_name='Activity')),
            ],
            options={
                'verbose_name': 'Activity attribute',
                'verbose_name_plural': 'Activity attributes',
            },
            bases=(landmatrix.models.default_string_representation.DefaultStringRepresentation, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalActivityAttribute',
            fields=[
                ('id', models.IntegerField(db_index=True, auto_created=True, blank=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, blank=True, null=True)),
                ('value', models.TextField(max_length=255, blank=True, null=True)),
                ('date', models.DateField(db_index=True, verbose_name='Date', blank=True, null=True)),
                ('polygon', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, blank=True, null=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('fk_activity', models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='landmatrix.Activity', blank=True, related_name='+')),
            ],
            options={
                'verbose_name': 'historical Activity attribute',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.RemoveField(
            model_name='historicalactivityattributegroup',
            name='fk_activity',
        ),
        migrations.RemoveField(
            model_name='historicalactivityattributegroup',
            name='fk_language',
        ),
        migrations.RemoveField(
            model_name='historicalactivityattributegroup',
            name='history_user',
        ),
        migrations.AlterModelOptions(
            name='activityattributegroup',
            options={'verbose_name': 'Activity attribute group', 'verbose_name_plural': 'Activity attribute groups'},
        ),
        migrations.RemoveField(
            model_name='activityattributegroup',
            name='attributes',
        ),
        migrations.RemoveField(
            model_name='activityattributegroup',
            name='date',
        ),
        migrations.RemoveField(
            model_name='activityattributegroup',
            name='fk_activity',
        ),
        migrations.RemoveField(
            model_name='activityattributegroup',
            name='fk_language',
        ),
        migrations.RemoveField(
            model_name='activityattributegroup',
            name='polygon',
        ),
        migrations.AddField(
            model_name='publicinterfacecache',
            name='is_public',
            field=models.BooleanField(db_index=True, default=False, verbose_name='Is this a public deal?'),
        ),
        migrations.AlterField(
            model_name='filtercondition',
            name='operator',
            field=models.CharField(max_length=10, verbose_name='Operator', choices=[('in', 'in'), ('is', 'is'), ('lte', 'lte'), ('gt', 'gt'), ('is_empty', 'is_empty'), ('contains', 'contains'), ('not_in', 'not_in'), ('lt', 'lt'), ('gte', 'gte')]),
        ),
        migrations.AlterIndexTogether(
            name='publicinterfacecache',
            index_together=set([('is_public', 'deal_scope'), ('is_public', 'deal_scope', 'negotiation_status'), ('is_public', 'deal_scope', 'negotiation_status', 'implementation_status'), ('is_public', 'deal_scope', 'implementation_status')]),
        ),
        migrations.DeleteModel(
            name='HistoricalActivityAttributeGroup',
        ),
        migrations.AddField(
            model_name='historicalactivityattribute',
            name='fk_group',
            field=models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='landmatrix.ActivityAttributeGroup', blank=True, related_name='+'),
        ),
        migrations.AddField(
            model_name='historicalactivityattribute',
            name='fk_language',
            field=models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='landmatrix.Language', blank=True, related_name='+'),
        ),
        migrations.AddField(
            model_name='historicalactivityattribute',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, related_name='+'),
        ),
        migrations.AddField(
            model_name='activityattribute',
            name='fk_group',
            field=models.ForeignKey(verbose_name='Activity Attribute Group', null=True, to='landmatrix.ActivityAttributeGroup', blank=True),
        ),
        migrations.AddField(
            model_name='activityattribute',
            name='fk_language',
            field=models.ForeignKey(verbose_name='Language', null=True, to='landmatrix.Language', blank=True),
        ),
        migrations.RemoveField(
            model_name='publicinterfacecache',
            name='is_deal',
        ),
    ]
