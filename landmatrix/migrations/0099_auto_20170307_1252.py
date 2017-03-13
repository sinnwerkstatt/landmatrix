# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0098_auto_20170307_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activityfeedback',
            name='fk_user_assigned',
            field=models.ForeignKey(blank=True, null=True, related_name='user_assigned', verbose_name='User assigned', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='activityfeedback',
            name='fk_user_created',
            field=models.ForeignKey(blank=True, null=True, related_name='user_created', verbose_name='User created', to=settings.AUTH_USER_MODEL),
        ),
    ]
