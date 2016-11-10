# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0095_auto_20161006_1026'),
    ]

    operations = [
        migrations.RenameField(
            model_name='filterpreset',
            old_name='is_default',
            new_name='is_default_country_region',
        ),
        migrations.RenameField(
            model_name='filterpreset',
            old_name='overrides_default',
            new_name='is_default_global',
        ),
        migrations.AddField(
            model_name='filterpreset',
            name='is_hidden',
            field=models.BooleanField(default=False, verbose_name='Is hidden'),
        ),
        migrations.AlterField(
            model_name='investorventureinvolvement',
            name='investment_type',
            field=multiselectfield.db.fields.MultiSelectField(default='', choices=[(10, 'Shares/Equity'), (20, 'Debt financing')], blank=True, max_length=255, null=True),
        ),
    ]
