# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailredirects', '0005_capitalizeverbose'),
        ('wagtailforms', '0003_capitalizeverbose'),
        ('wagtailcore', '0023_alter_page_revision_on_delete_behaviour'),
        ('landmatrix', '0037_wagtailhomepage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wagtailhomepage',
            name='page_ptr',
        ),
        migrations.DeleteModel(
            name='WagtailHomePage',
        ),
    ]
