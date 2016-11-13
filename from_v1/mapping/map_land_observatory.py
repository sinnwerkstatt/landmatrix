from landmatrix.models.investor import Investor
from .land_observatory_objects.tag_groups import A_Tag_Group, SH_Tag_Group
from .land_observatory_objects.stakeholder import Stakeholder
from .land_observatory_objects.changeset import Changeset
from .land_observatory_objects.involvement import Involvement
from .map_lo_model import MapLOModel
from .map_lo_activities import MapLOActivities
from .map_lo_stakeholder import MapLOStakeholder
from .map_lo_involvements import MapLOInvolvements

from migrate import V2

from django.db import transaction



class MapLandObservatory:
    """
    Preparing the land observatory data:
    cat cdelokp-unibe-ch_data_20160510.backup | sed s/lokpeditor/<db_user>/g > cdelokp-unibe-ch_data_20160510.backup.lm
    pg_restore -c cdelokp-unibe-ch_data_20160510.backup.lm
    psql -U<db_user> -c 'ALTER USER <db_user> SET SEARCH_PATH = data, public;'
    """

    @classmethod
    def map_all(cls, save=False, verbose=False):
        with transaction.atomic(using=V2):
            MapLOActivities.cleanup_previously_imported_rejected_deals(
                save=save, verbose=verbose)
            MapLOInvolvements.cleanup_previously_imported_involvements(
                save=save, verbose=verbose)
            MapLOStakeholder.map_all(save, verbose)
            MapLOActivities.map_all(save, verbose)
            MapLOInvolvements.map_all(save, verbose)
            # MapLOChangesets.map_all(save, verbose)


class MapLOChangesets(MapLOModel):

    old_class = Changeset

    @classmethod
    def all_records(cls):
        return Changeset.objects.using('lo').all().values()

    @classmethod
    def save_record(cls, new, save):
        print(new)
