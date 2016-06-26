# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0004_auto_20160509_1530'),
    ]

    operations = [
        migrations.AddField(
            model_name='userregionalinfo',
            name='phone',
            field=models.CharField(null=True, max_length=255, blank=True),
        ),
    ]
