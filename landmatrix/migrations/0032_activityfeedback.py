# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('landmatrix', '0031_auto_20160113_1144'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityFeedback',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.TextField(verbose_name='Comment')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Timestamp')),
                ('fk_activity', models.ForeignKey(verbose_name='Activity', to='landmatrix.Activity')),
                ('fk_user_assigned', models.ForeignKey(verbose_name='User assigned', related_name='user_assigned', to=settings.AUTH_USER_MODEL)),
                ('fk_user_created', models.ForeignKey(verbose_name='User created', related_name='user_created', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
