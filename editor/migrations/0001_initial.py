# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-05-18 16:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('landmatrix', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRegionalInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.ManyToManyField(blank=True, to='landmatrix.Country')),
                ('region', models.ManyToManyField(blank=True, to='landmatrix.Region')),
                ('super_user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='super_user', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('editor', 'Editor'), ('editor_filter', 'Filter dashboard')),
            },
        ),
    ]
