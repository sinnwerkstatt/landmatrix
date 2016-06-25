# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0079_filtercondition_key'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='filterpreset',
            options={'verbose_name': 'Filter preset', 'verbose_name_plural': 'Filter presets'},
        ),
        migrations.AlterModelOptions(
            name='filterpresetgroup',
            options={'verbose_name': 'Filter preset group', 'verbose_name_plural': 'Filter preset groups'},
        ),
        migrations.AddField(
            model_name='filterpreset',
            name='relation',
            field=models.CharField(default='and', choices=[('and', 'And'), ('or', 'Or')], max_length=3),
        ),
        migrations.AlterField(
            model_name='filtercondition',
            name='key',
            field=models.CharField(default='value', choices=[('value', 'Value'), ('value2', 'Value 2'), ('date', 'Date'), ('polygon', 'Polygon'), ('high_income', 'High income')], max_length=32, verbose_name='Key'),
        ),
    ]
