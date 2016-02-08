# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0032_activityfeedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityChangeset',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('comment', models.TextField(verbose_name='Comment')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Timestamp')),
                ('source', models.TextField(null=True, blank=True, verbose_name='Source')),
                ('fk_activity', models.ForeignKey(to='landmatrix.Activity', verbose_name='Activity')),
            ],
        ),
        migrations.AlterField(
            model_name='activityfeedback',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID'),
        ),
    ]
