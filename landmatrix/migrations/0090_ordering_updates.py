# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0089_cleanup_activity_changeset'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activitychangeset',
            options={'ordering': ('-timestamp',)},
        ),
        migrations.AlterModelOptions(
            name='activityfeedback',
            options={'verbose_name_plural': 'Activity feedbacks', 'verbose_name': 'Activity feedback', 'ordering': ('-timestamp', '-id')},
        ),
    ]
