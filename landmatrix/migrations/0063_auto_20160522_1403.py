# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def create_filter_preset_groups(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    FilterPreset = apps.get_model("landmatrix", "FilterPreset")
    FilterPresetGroup = apps.get_model("landmatrix", "FilterPresetGroup")
    for preset in FilterPreset.objects.all():
        group, created = FilterPresetGroup.objects.get_or_create(
            name=preset.old_group,
        )
        preset.group = group
        preset.save()


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0062_auto_20160509_1709'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilterPresetGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='filtercondition',
            name='operator',
            field=models.CharField(max_length=10, choices=[('gt', 'gt'), ('gte', 'gte'), ('lt', 'lt'), ('is', 'is'), ('lte', 'lte'), ('not_in', 'not_in'), ('contains', 'contains'), ('in', 'in'), ('is_empty', 'is_empty')], verbose_name='Operator'),
        ),
        migrations.AlterField(
            model_name='filtercondition',
            name='variable',
            field=models.CharField(max_length=32, verbose_name='Variable'),
        ),
        migrations.RenameField(
            model_name='filterpreset',
            old_name='group',
            new_name='old_group'
        ),
        migrations.AddField(
            model_name='filterpreset',
            name='group',
            field=models.ForeignKey(to='landmatrix.FilterPresetGroup', null=True),
        ),
        migrations.RunPython(create_filter_preset_groups),


    ]
