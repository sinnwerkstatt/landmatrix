# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0002_auto_20160125_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='userregionalinfo',
            name='super_user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, blank=True, null=True, related_name='super_user'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userregionalinfo',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
