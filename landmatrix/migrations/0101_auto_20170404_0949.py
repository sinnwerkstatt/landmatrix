# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0100_auto_20170307_1252'),
    ]

    operations = [
        migrations.RenameField(
            model_name='filterpreset',
            old_name='is_default_country_region',
            new_name='is_default_country',
        ),
    ]
