# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def fully_updated_to_boolean(apps, schema_editor):
    Activity = apps.get_model("landmatrix", "Activity")
    HistoricalActivity = apps.get_model("landmatrix", "HistoricalActivity")
    for activity in Activity.objects.all():
        activity.fully_updated = activity.fully_updated_old and 't' or 'f'
        activity.save()
    for activity in HistoricalActivity.objects.all():
        activity.fully_updated = activity.fully_updated_old and 't' or 'f'
        activity.save()

class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0082_auto_20160626_2015'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activityfeedback',
            options={'verbose_name': 'Activity feedback', 'verbose_name_plural': 'Activity feedbacks'},
        ),
        migrations.AlterField(
            model_name='activityfeedback',
            name='fk_activity',
            field=models.ForeignKey(verbose_name='Activity', to='landmatrix.HistoricalActivity'),
        ),
        migrations.RenameField(
            model_name='activity',
            old_name='fully_updated',
            new_name='fully_updated_old',
        ),
        migrations.RenameField(
            model_name='historicalactivity',
            old_name='fully_updated',
            new_name='fully_updated_old',
        ),
        migrations.AddField(
            model_name='activity',
            name='fully_updated',
            field=models.BooleanField(default=False, verbose_name='Fully updated'),
        ),
        migrations.AddField(
            model_name='historicalactivity',
            name='fully_updated',
            field=models.BooleanField(default=False, verbose_name='Fully updated'),
        ),
        migrations.RunPython(fully_updated_to_boolean),
    ]
