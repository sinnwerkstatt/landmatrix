# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('landmatrix', '0030_auto_20151209_1447'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRegionalInfo',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('country', models.ManyToManyField(to='landmatrix.Country')),
                ('region', models.ManyToManyField(to='landmatrix.Region')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
