# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationEmail',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('sent_on', models.DateTimeField(editable=False, null=True, verbose_name='Sent on', blank=True)),
                ('sent_status', models.PositiveSmallIntegerField(editable=False, default=1, choices=[(1, 'New'), (2, 'Sent'), (3, 'Error')])),
                ('sent_exception', models.TextField(blank=True)),
                ('to', models.TextField(verbose_name='To')),
                ('cc', models.TextField(verbose_name='CC', blank=True)),
                ('bcc', models.TextField(verbose_name='BCC', blank=True)),
                ('reply_to', models.TextField(verbose_name='Reply To', blank=True)),
                ('subject', models.CharField(max_length=255, verbose_name='Subject', blank=True)),
                ('from_email', models.CharField(max_length=255, verbose_name='From', blank=True)),
                ('body_text', models.TextField(verbose_name='Body Plain Text')),
                ('body_html', models.TextField(verbose_name='Body HTML', blank=True)),
            ],
        ),
    ]
