# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0074_auto_20160618_1620'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historicalinvestor',
            options={'verbose_name': 'Historical investor', 'verbose_name_plural': 'Historical investors', 'get_latest_by': 'history_date'},
        ),
        migrations.AlterModelOptions(
            name='investor',
            options={'verbose_name': 'Investor', 'verbose_name_plural': 'Investors'},
        ),
        migrations.RemoveField(
            model_name='historicalinvestor',
            name='history_id',
        ),
        migrations.RemoveField(
            model_name='historicalinvestor',
            name='history_type',
        ),
        migrations.AlterField(
            model_name='historicalinvestor',
            name='fk_country',
            field=models.ForeignKey(null=True, blank=True, to='landmatrix.Country', verbose_name='Country of registration/origin'),
        ),
        migrations.AlterField(
            model_name='historicalinvestor',
            name='fk_status',
            field=models.ForeignKey(to='landmatrix.Status', verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='historicalinvestor',
            name='history_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='historicalinvestor',
            name='history_user',
            field=models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='historicalinvestor',
            name='id',
            field=models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True),
        ),
        migrations.AlterField(
            model_name='historicalinvestor',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Timestamp'),
        ),
    ]
