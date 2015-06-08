# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.postgres.operations import HStoreExtension

class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0007_auto_20150608_1128'),
    ]

    operations = [
        HStoreExtension()
    ]
