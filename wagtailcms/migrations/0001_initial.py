# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0023_alter_page_revision_on_delete_behaviour'),
    ]

    operations = [
        migrations.CreateModel(
            name='WagtailPage',
            fields=[
                ('page_ptr', models.OneToOneField(primary_key=True, auto_created=True, parent_link=True, to='wagtailcore.Page', serialize=False)),
                ('body', wagtail.wagtailcore.fields.RichTextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='WagtailRootPage',
            fields=[
                ('page_ptr', models.OneToOneField(primary_key=True, auto_created=True, parent_link=True, to='wagtailcore.Page', serialize=False)),
                ('footer_column_1', wagtail.wagtailcore.fields.RichTextField(blank=True)),
                ('footer_column_2', wagtail.wagtailcore.fields.RichTextField(blank=True)),
                ('footer_column_3', wagtail.wagtailcore.fields.RichTextField(blank=True)),
                ('footer_column_4', wagtail.wagtailcore.fields.RichTextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
