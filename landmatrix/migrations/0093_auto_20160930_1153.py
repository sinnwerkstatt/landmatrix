# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0092_populate_activity_rel'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='investor',
            options={'ordering': ('name',), 'verbose_name_plural': 'Investors', 'verbose_name': 'Investor'},
        ),
        migrations.AlterField(
            model_name='investorventureinvolvement',
            name='investment_type',
            field=models.CommaSeparatedIntegerField(null=True, max_length=255, choices=[(10, 'Shares/Equity'), (20, 'Debt financing')], blank=True),
        ),
    ]
