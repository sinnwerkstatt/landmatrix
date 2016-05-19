from .land_observatory_objects.tag_groups import A_Tag_Group, SH_Tag_Group
from .land_observatory_objects.activity import Activity
from .land_observatory_objects.stakeholder import Stakeholder
from .land_observatory_objects.changeset import Changeset
from .land_observatory_objects.involvement import Involvement

from migrate import V1, V2

from django.db import transaction

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class MapLandObservatory:
    """
    Preparing the land observatory data:
    cat cdelokp-unibe-ch_data_20160510.backup | sed s/lokpeditor/<db_user>/g > cdelokp-unibe-ch_data_20160510.backup.lm
    pg_restore -c cdelokp-unibe-ch_data_20160510.backup.lm
    psql -U<db_user> -c 'ALTER USER <db_user> SET SEARCH_PATH = data, public;'
    """

    @classmethod
    @transaction.atomic(using=V2)
    def map_all(cls, save=False, verbose=False):
        MapLOActivities.map_all(save, verbose)
        MapLOATagGroups.map_all(save, verbose)
        MapLOStakeholders.map_all(save, verbose)
        MapLOSTagGroups.map_all(save, verbose)
        MapLOChangesets.map_all(save, verbose)
        MapLOInvolvements.map_all(save, verbose)


def map_status_id(id):
    return id


class MapLOActivities:

    attributes = {
        'fk_status': ('fk_status_id', map_status_id),
    }
    activities = Activity.objects.using('lo').all()

    @classmethod
    def map_all(cls, save=False, verbose=False):
        print(cls.activities)


class MapLOATagGroups:

    tag_groups = A_Tag_Group.objects.using('lo').all()

    @classmethod
    def map_all(cls, save=False, verbose=False):
        for tg in cls.tag_groups:
            print(tg)


class MapLOStakeholders:

    stakeholders = Stakeholder.objects.using('lo').all()

    @classmethod
    def map_all(cls, save=False, verbose=False):
        print(cls.stakeholders)


class MapLOSTagGroups:

    tag_groups = SH_Tag_Group.objects.using('lo').all()

    @classmethod
    def map_all(cls, save=False, verbose=False):
        for tg in cls.tag_groups:
            print(tg)


class MapLOChangesets:

    changesets = Changeset.objects.using('lo').all()

    @classmethod
    def map_all(cls, save=False, verbose=False):
        print(cls.changesets)

class MapLOInvolvements:

    involvements = Involvement.objects.using('lo').all()

    @classmethod
    def map_all(cls, save=False, verbose=False):
        for tg in cls.involvements:
            print(tg)
