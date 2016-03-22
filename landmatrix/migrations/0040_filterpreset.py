# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0039_auto_20160322_1527'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilterPreset',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('is_default', models.BooleanField(default=False)),
                ('overrides_default', models.BooleanField(default=False)),
            ],
        ),
    ]
