# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0017_currency'),
    ]

    operations = [
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('code', models.CharField(verbose_name='Code', max_length=255)),
                ('name', models.CharField(verbose_name='Name', max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='currency',
            name='id',
            field=models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False),
            preserve_default=True,
        ),
    ]
