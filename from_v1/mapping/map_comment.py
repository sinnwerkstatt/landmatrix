from pprint import pprint

from from_v1.migrate import V1, V2
from .map_model import MapModel
from .map_activity_tag_group import MapActivityTagGroup
from .map_stakeholder_investor import MapStakeholderInvestor

import landmatrix.models
import old_editor.models

from django.db import transaction


def map_tag_group_id(tag_group_id):
    id = MapActivityTagGroup.tag_group_to_attribute_group_ids.get(tag_group_id)
    if not landmatrix.models.ActivityAttributeGroup.objects.using(V2).filter(id=id).exists():
        id = None
    return id

class MapComment(MapModel):
    old_class = old_editor.models.Comment
    new_class = landmatrix.models.Comment
    attributes = {
        'fk_a_tag_group_id': ('fk_activity_attribute_group_id', map_tag_group_id),
    }

    @classmethod
    def all_records(cls):
        return cls.old_class.objects.using(V1).filter(fk_a_tag_group__isnull=False).exclude(comment='').values()

    @classmethod
    @transaction.atomic(using=V2)
    def map_all(cls, save=False, verbose=False):

        # pprint(MapActivityTagGroup.tag_group_to_attribute_group_ids)
        cls._check_dependencies()
        cls._start_timer()

        comments = cls.all_records()
        cls._count = len(comments)
        for index, record in enumerate(comments):
            cls.map_record(record, save, verbose)
            cls._print_status(record, index)

        cls._done = True
        cls._print_summary()


def map_sh_tag_group_id(tag_group_id):
    id = MapActivityTagGroup.tag_group_to_attribute_group_ids.get(tag_group_id)
    if not landmatrix.models.ActivityAttributeGroup.objects.using(V2).filter(id=id).exists():
        id = None
    return id


class MapStakeholderComment(MapComment):

    attributes = {
        'fk_sh_tag_group_id': ('fk_activity_attribute_group_id', map_sh_tag_group_id),
    }
    depends = [MapStakeholderInvestor]

    @classmethod
    def map_record(cls, record, save=False, verbose=False):
        sh_tag_group = old_editor.models.SH_Tag_Group.objects.using(V1).get(
            id=record['fk_sh_tag_group_id']
        )
        investor = landmatrix.models.Investor.objects.using(V2).get(
            pk=sh_tag_group.fk_stakeholder_id
        )
        investor.comment = record['comment']
        if save:
            investor.save(using=V2)

    @classmethod
    def all_records(cls):
        return cls.old_class.objects.using(V1).filter(fk_sh_tag_group__isnull=False).exclude(comment='').values()
