# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def add_names_to_unknown_investors(apps, schema_editor):
    Investor = apps.get_model("landmatrix", "Investor")
    db_alias = schema_editor.connection.alias
    for investor in Investor.objects.filter(name=''):
        investor.name = "Unknown (#%s)" % (investor.pk,)
        investor.save()


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0064_auto_20160524_1718'),
    ]

    operations = [
        migrations.RunPython(add_names_to_unknown_investors,
                             migrations.RunPython.noop),
    ]
