# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0078_auto_20160624_2338'),
    ]

    operations = [
        migrations.AddField(
            model_name='filtercondition',
            name='key',
            field=models.CharField(max_length=32, choices=[('value', 'Value'), ('value2', 'Value 2'), ('date', 'Date'), ('polygon', 'Polygon')], verbose_name='Key', default='value'),
        ),
    ]
