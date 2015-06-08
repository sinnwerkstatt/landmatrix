# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def insert_statuses(apps, schema_editor):
    status_names = ['pending', 'active', 'overwritten', 'deleted', 'rejected', 'to_delete']
    Status = apps.get_model("landmatrix", "Status")
    for name in status_names:
        Status(name=name).save()


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0005_status'),
    ]

    operations = [
        migrations.RunPython(insert_statuses),
    ]
