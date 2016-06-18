# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings

def update_historical_activity_attribute(apps, schema_editor):
    HistoricalActivityAttribute = apps.get_model("landmatrix", "HistoricalActivityAttribute")
    db_alias = schema_editor.connection.alias
    for attribute in HistoricalActivityAttribute.objects.all():
        attribute.id = attribute.history_id
        attribute.save()

def update_historical_activity(apps, schema_editor):
    HistoricalActivity = apps.get_model("landmatrix", "HistoricalActivity")
    HistoricalActivityAttribute = apps.get_model("landmatrix", "HistoricalActivityAttribute")
    db_alias = schema_editor.connection.alias
    for activity in HistoricalActivity.objects.all():
        for attribute in HistoricalActivityAttribute.objects.filter(fk_activity_id=activity.id):
            attribute.fk_activity_id = activity.history_id
            attribute.save()
        activity.id = activity.history_id
        activity.save()

class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0073_auto_20160615_2205'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activity',
            options={'verbose_name_plural': 'Activities', 'verbose_name': 'Activity'},
        ),
        migrations.AlterModelOptions(
            name='historicalactivity',
            options={'verbose_name_plural': 'Historical activities', 'get_latest_by': 'history_date', 'verbose_name': 'Historical activity'},
        ),
        migrations.AlterModelOptions(
            name='historicalactivityattribute',
            options={'verbose_name_plural': 'Historical activity attributes', 'verbose_name': 'Historical activity attribute'},
        ),
        migrations.RemoveField(
            model_name='historicalactivity',
            name='history_type',
        ),
        migrations.RemoveField(
            model_name='historicalactivityattribute',
            name='history_type',
        ),
        migrations.AlterField(
            model_name='activity',
            name='fk_status',
            field=models.ForeignKey(default=1, to='landmatrix.Status', verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='activityattribute',
            name='fk_group',
            field=models.ForeignKey(null=True, blank=True, to='landmatrix.ActivityAttributeGroup', verbose_name='Activity Attribute Group'),
        ),
        migrations.AlterField(
            model_name='historicalactivity',
            name='fk_status',
            field=models.ForeignKey(default=1, to='landmatrix.Status', verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='historicalactivity',
            name='fully_updated',
            field=models.DateTimeField(null=True, auto_now_add=True, verbose_name='Fully updated'),
        ),
        migrations.AlterField(
            model_name='historicalactivity',
            name='history_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='historicalactivity',
            name='history_user',
            field=models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL),
        ),
        #migrations.RunPython(update_historical_activity),
        migrations.RemoveField(
            model_name='historicalactivity',
            name='history_id',
        ),
        migrations.AlterField(
            model_name='historicalactivity',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='historicalactivityattribute',
            name='fk_activity',
            field=models.ForeignKey(related_name='history_attributes', to='landmatrix.HistoricalActivity', verbose_name='Activity'),
        ),
        migrations.AlterField(
            model_name='historicalactivityattribute',
            name='fk_group',
            field=models.ForeignKey(null=True, blank=True, to='landmatrix.ActivityAttributeGroup', verbose_name='Activity Attribute Group'),
        ),
        migrations.AlterField(
            model_name='historicalactivityattribute',
            name='fk_language',
            field=models.ForeignKey(null=True, blank=True, to='landmatrix.Language', verbose_name='Language'),
        ),
        migrations.RemoveField(
            model_name='historicalactivityattribute',
            name='history_date',
        ),
        migrations.RemoveField(
            model_name='historicalactivityattribute',
            name='history_user',
        ),
        #migrations.RunPython(update_historical_activity_attribute),
        migrations.RemoveField(
            model_name='historicalactivityattribute',
            name='history_id',
        ),
        migrations.AlterField(
            model_name='historicalactivityattribute',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID'),
        ),

    ]
