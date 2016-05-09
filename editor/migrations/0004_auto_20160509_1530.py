# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0003_auto_20160125_1756'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userregionalinfo',
            options={'permissions': (('editor', 'Editor'), ('editor_filter', 'Filter dashboard'))},
        ),
    ]
