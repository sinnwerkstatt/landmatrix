import reversion
from django.contrib.auth import get_user_model

from apps.greennewdeal.models import Deal
from apps.greennewdeal.synchronization.deal import base, submodels
from apps.greennewdeal.synchronization.helpers import MetaActivity
from apps.landmatrix.models import HistoricalActivity

#              1        2           3           4       5          6
# Stati old: Pending, Active, Overwritten,  Deleted, Rejected, To_delete
# Stati new: Draft,   Live,   Live+Draft,   Deleted, Rejected, To_delete
STATUS_MAP = {1: 1, 2: 2, 3: 2, 4: 4, 5: 5, 6: 6}


def histivity_to_deal(activity_pk: int = None, activity_identifier: int = None):
    if activity_pk and activity_identifier:
        raise AttributeError("just specify one")
    elif activity_pk:
        activity_versions = HistoricalActivity.objects.filter(pk=activity_pk)
    elif activity_identifier:
        activity_versions = HistoricalActivity.objects.filter(
            activity_identifier=activity_identifier
        ).order_by("pk")
    else:
        raise AttributeError("specify activity_pk or activity_identifier")

    if not activity_versions:
        return

    try:
        deal = Deal.objects.get(id=activity_versions[0].activity_identifier)
    except Deal.DoesNotExist:
        deal = Deal(id=activity_versions[0].activity_identifier)

    for histivity in activity_versions:
        meta_activity = MetaActivity(histivity)
        with reversion.create_revision():
            submodels.create_locations(
                deal, meta_activity.loc_groups, timestamp=histivity.history_date
            )
            submodels.create_contracts(
                deal, meta_activity.con_groups, timestamp=histivity.history_date
            )
            submodels.create_data_sources(
                deal, meta_activity.ds_groups, timestamp=histivity.history_date
            )

            base.parse_general(deal, meta_activity.group_general)
            base.parse_employment(deal, meta_activity.group_employment)

            base.connect_investor_to_deal(deal, histivity)

            base.parse_investor_info(deal, meta_activity.group_investor_info)
            base.parse_local_communities(deal, meta_activity.group_local_communities)
            base.parse_former_use(deal, meta_activity.group_former_use)
            base.parse_produce_info(deal, meta_activity.group_produce_info)
            base.parse_water(deal, meta_activity.group_water)
            base.parse_remaining(deal, meta_activity.group_remaining)

            status = STATUS_MAP[histivity.fk_status_id]
            deal.timestamp = histivity.history_date
            deal.save_revision(
                status,
                histivity.history_date,
                get_user_model().objects.filter(id=histivity.history_user_id).first(),
                histivity.comment or "",
            )
