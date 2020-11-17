import reversion
from django.contrib.auth import get_user_model

from apps.landmatrix.models import Deal
from apps.landmatrix.synchronization.deal import base, submodels
from apps.landmatrix.synchronization.helpers import MetaActivity
from apps.landmatrix.models import HistoricalActivity


def histivity_to_deal(activity_pk: int = None, activity_identifier: int = None):
    if activity_pk and activity_identifier:
        raise AttributeError("just specify one")
    elif activity_pk:
        activity_versions = HistoricalActivity.objects.filter(pk=activity_pk)
        activity_identifier = activity_versions[0].activity_identifier
    elif activity_identifier:
        activity_versions = HistoricalActivity.objects.filter(
            activity_identifier=activity_identifier
        ).order_by("pk")
    else:
        raise AttributeError("specify activity_pk or activity_identifier")

    if not activity_versions:
        return

    for histivity in activity_versions:
        try:
            deal = Deal.objects.get(id=activity_identifier)
            is_new_deal = False
        except Deal.DoesNotExist:
            deal = Deal(id=activity_identifier)
            is_new_deal = True

        meta_activity = MetaActivity(histivity)
        with reversion.create_revision():
            if is_new_deal:
                deal.created_at = histivity.history_date

            deal.modified_at = histivity.history_date

            submodels.create_locations(deal, meta_activity.loc_groups)
            submodels.create_contracts(deal, meta_activity.con_groups)
            submodels.create_data_sources(deal, meta_activity.ds_groups)

            base.parse_general(deal, meta_activity.group_general)
            base.parse_employment(deal, meta_activity.group_employment)

            base.connect_investor_to_deal(deal, histivity)

            base.parse_investor_info(deal, meta_activity.group_investor_info)
            base.parse_local_communities(deal, meta_activity.group_local_communities)
            base.parse_former_use(deal, meta_activity.group_former_use)
            base.parse_produce_info(deal, meta_activity.group_produce_info)
            base.parse_water(deal, meta_activity.group_water)
            base.parse_remaining(deal, meta_activity.group_remaining)

            deal.save_revision(
                status=histivity.fk_status_id,
                date=histivity.history_date,
                user=get_user_model()
                .objects.filter(id=histivity.history_user_id)
                .first(),
                comment=histivity.comment or "",
            )
