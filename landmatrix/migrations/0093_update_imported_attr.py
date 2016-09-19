# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid

from django.db import migrations
from django.utils import timezone


def update_imported_activity_attributes(apps, schema_editor):
    ActivityAttributeGroup = apps.get_model(
        'landmatrix', 'ActivityAttributeGroup')
    ActivityAttribute = apps.get_model('landmatrix', 'ActivityAttribute')
    HistoricalActivityAttribute = apps.get_model(
        'landmatrix', 'HistoricalActivityAttribute')

    imported_aag,  _ = ActivityAttributeGroup.objects.get_or_create(
        name='imported')
    data_source_comments = ActivityAttribute.objects.filter(
        name='tg_data_source_comment')
    historical_data_source_comments = HistoricalActivityAttribute.objects.filter(
        name='tg_data_source_comment')
    # This isn't the real import time, but keep it all the same so it's easy
    # to group things
    import_time = timezone.now().isoformat()

    for queryset in (data_source_comments, historical_data_source_comments):
        for comment_attr in queryset:
            try:
                uuid.UUID(comment_attr.value)
            except ValueError:
                # Must be an actual comment, not an imported string
                pass
            else:
                # convert the comment
                queryset.model.objects.create(
                    fk_group=imported_aag,
                    fk_language=comment_attr.fk_language,
                    fk_activity=comment_attr.fk_activity, name='id',
                    value=comment_attr.value)
                queryset.model.objects.create(
                    fk_group=imported_aag,
                    fk_language=comment_attr.fk_language,
                    fk_activity=comment_attr.fk_activity, name='source',
                    value='Land Observatory')
                queryset.model.objects.create(
                    fk_group=imported_aag,
                    fk_language=comment_attr.fk_language,
                    fk_activity=comment_attr.fk_activity, name='timestamp',
                    value=import_time)

                # delete the old comment
                comment_attr.delete()


def reverse_imported_activity_attributes(apps, schema_editor):
    ActivityAttributeGroup = apps.get_model(
        'landmatrix', 'ActivityAttributeGroup')
    ActivityAttribute = apps.get_model('landmatrix', 'ActivityAttribute')
    HistoricalActivityAttribute = apps.get_model(
        'landmatrix', 'HistoricalActivityAttribute')

    data_source_aag = ActivityAttributeGroup.objects.get(name='data_source_0')
    imported_ids = ActivityAttribute.objects.filter(
        fk_group__name='imported', name='id')
    imported_historical_ids = HistoricalActivityAttribute.objects.filter(
        fk_group__name='imported', name='id')

    for queryset in (imported_ids, imported_historical_ids):
        for id_attr in queryset:
            queryset.model.objects.create(
                fk_group=data_source_aag,
                fk_language=id_attr.fk_language,
                fk_activity=id_attr.fk_activity, name='tg_data_source_comment',
                value=id_attr.value)

            id_attr.delete()

    ActivityAttribute.objects.filter(
        fk_group__name='imported', name='source').delete()
    ActivityAttribute.objects.filter(
        fk_group__name='imported', name='timestamp').delete()

    HistoricalActivityAttribute.objects.filter(
        fk_group__name='imported', name='source').delete()
    HistoricalActivityAttribute.objects.filter(
        fk_group__name='imported', name='timestamp').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0092_populate_activity_rel'),
    ]

    operations = [
        migrations.RunPython(
            update_imported_activity_attributes,
            reverse_imported_activity_attributes),
    ]
