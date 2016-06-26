# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings

def move_changeset_to_historical_activity(apps, schema_editor):
    ActivityChangeset = apps.get_model("landmatrix", "ActivityChangeset")
    HistoricalActivity = apps.get_model("landmatrix", "HistoricalActivity")
    for changeset in ActivityChangeset.objects.all():
        activity = changeset.fk_activity
        activity.comment = changeset.comment
        activity.save()

def move_review_to_changeset(apps, schema_editor):
    ActivityChangesetReview = apps.get_model("landmatrix", "ActivityChangesetReview")
    ActivityChangeset = apps.get_model("landmatrix", "ActivityChangeset")
    db_alias = schema_editor.connection.alias
    for review in ActivityChangesetReview.objects.all():
        changeset = review.fk_activity_changeset
        changeset.fk_user = review.fk_user
        #changeset.country = review.country
        #changeset.region = review.region
        changeset.timestamp = review.timestamp
        changeset.fk_review_decision = review.fk_review_decision
        changeset.comment = review.comment
        changeset.save()

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('landmatrix', '0081_auto_20160626_1934'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitychangeset',
            name='country',
            field=models.ForeignKey(to='landmatrix.Country', blank=True, null=True, verbose_name='County'),
        ),
        migrations.AddField(
            model_name='activitychangeset',
            name='fk_review_decision',
            field=models.ForeignKey(to='landmatrix.ReviewDecision', blank=True, null=True, verbose_name='Review decision'),
        ),
        migrations.AddField(
            model_name='activitychangeset',
            name='fk_user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True, verbose_name='User'),
        ),
        migrations.AddField(
            model_name='activitychangeset',
            name='region',
            field=models.ForeignKey(to='landmatrix.Region', blank=True, null=True, verbose_name='Region'),
        ),
        migrations.AddField(
            model_name='historicalactivity',
            name='comment',
            field=models.TextField(null=True, verbose_name='Comment', blank=True),
        ),
        migrations.AlterField(
            model_name='activitychangeset',
            name='comment',
            field=models.TextField(null=True, verbose_name='Comment', blank=True),
        ),
        migrations.RunPython(move_changeset_to_historical_activity),
        migrations.RunPython(move_review_to_changeset),
        migrations.RemoveField(
            model_name='activitychangesetreview',
            name='fk_activity_changeset',
        ),
        migrations.RemoveField(
            model_name='activitychangesetreview',
            name='fk_review_decision',
        ),
        migrations.RemoveField(
            model_name='activitychangesetreview',
            name='fk_user',
        ),
        migrations.DeleteModel(
            name='ActivityChangesetReview',
        ),
    ]
