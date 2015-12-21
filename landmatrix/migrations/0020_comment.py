# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('landmatrix', '0019_mineral'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.TextField(verbose_name='Comment')),
                ('timestamp', models.DateTimeField(verbose_name='Timestamp', auto_now_add=True)),
                ('fk_activity', models.ForeignKey(blank=True, to='landmatrix.Activity', verbose_name='Activity', null=True)),
                ('fk_activity_attribute_group', models.ForeignKey(blank=True, to='landmatrix.ActivityAttributeGroup', verbose_name='Activity attribute group', null=True)),
                ('fk_stakeholder_attribute_group', models.ForeignKey(blank=True, to='landmatrix.StakeholderAttributeGroup', verbose_name='Stakeholder attribute group', null=True)),
                ('fk_user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='User', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
