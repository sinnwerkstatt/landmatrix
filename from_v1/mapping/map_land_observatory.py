from .land_observatory_objects.tag_groups import A_Tag_Group, SH_Tag_Group
from .land_observatory_objects.activity import Activity
from .land_observatory_objects.stakeholder import Stakeholder
from .land_observatory_objects.changeset import Changeset
from .land_observatory_objects.involvement import Involvement
from .map_model import MapModel

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


class MapLOModel(MapModel):

    DB = 'lo'

    @classmethod
    def map_record(cls, record, save=False, verbose=False):
        print(record)
        

def map_status_id(id):
    return id


class MapLOActivities(MapLOModel):

    old_class = Activity
    attributes = {
        'fk_status': ('fk_status_id', map_status_id),
    }

    @classmethod
    def all_records(cls):
        return Activity.objects.using('lo').all().values()


class MapLOATagGroups(MapLOModel):

    old_class = A_Tag_Group

    @classmethod
    def all_records(cls):
        return A_Tag_Group.objects.using('lo').all().values()


class MapLOStakeholders(MapLOModel):

    old_class = Stakeholder

    @classmethod
    def all_records(cls):
        return Stakeholder.objects.using('lo').all().values()


class MapLOSTagGroups(MapLOModel):

    old_class = SH_Tag_Group

    @classmethod
    def all_records(cls):
        return SH_Tag_Group.objects.using('lo').all().values()


class MapLOChangesets(MapLOModel):

    old_class = Changeset

    @classmethod
    def all_records(cls):
        return Changeset.objects.using('lo').all().values()


class MapLOInvolvements(MapLOModel):

    old_class = Involvement

    @classmethod
    def all_records(cls):
        return Involvement.objects.using('lo').all().values()

