# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('landmatrix', '0033_auto_20160204_1649'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityChangesetReview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('timestamp', models.DateTimeField(verbose_name='Timestamp', auto_now_add=True)),
                ('comment', models.TextField(blank=True, verbose_name='Comment', null=True)),
                ('fk_activity_changeset', models.ForeignKey(verbose_name='Activity changeset', to='landmatrix.ActivityChangeset')),
            ],
        ),
        migrations.CreateModel(
            name='ReviewDecision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='Name', max_length=255)),
                ('description', models.TextField(verbose_name='Description')),
            ],
        ),
        migrations.AddField(
            model_name='activitychangesetreview',
            name='fk_review_decision',
            field=models.ForeignKey(verbose_name='Review decision', to='landmatrix.ReviewDecision'),
        ),
        migrations.AddField(
            model_name='activitychangesetreview',
            name='fk_user',
            field=models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL),
        ),
    ]
