from django.contrib.auth import get_user_model

from apps.landmatrix.models import Deal
from apps.landmatrix.models.versions import Revision, Version
from apps.landmatrix.synchronization.deal import base, submodels
from apps.landmatrix.synchronization.helpers import MetaActivity, calculate_new_stati
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
        deal, created = Deal.objects.get_or_create(id=activity_identifier)

        meta_activity = MetaActivity(histivity)

        if created:
            deal.created_at = histivity.history_date
        deal.modified_at = histivity.history_date
        deal.fully_updated = histivity.fully_updated
        if deal.fully_updated:
            deal.fully_updated_at = deal.modified_at

        base.parse_general(deal, meta_activity.group_general)
        base.parse_employment(deal, meta_activity.group_employment)

        base.connect_investor_to_deal(deal, histivity)

        base.parse_investor_info(deal, meta_activity.group_investor_info)
        base.parse_local_communities(deal, meta_activity.group_local_communities)
        base.parse_former_use(deal, meta_activity.group_former_use)
        base.parse_produce_info(deal, meta_activity.group_produce_info)
        base.parse_water(deal, meta_activity.group_water)
        base.parse_remaining(deal, meta_activity.group_remaining)

        new_status = histivity.fk_status_id
        rev1 = Revision.objects.create(
            date_created=histivity.history_date,
            user=get_user_model().objects.filter(id=histivity.history_user_id).first(),
            comment=histivity.comment or "",
        )

        do_save = deal.status == 1 or new_status in [2, 3, 4]

        if new_status != 4:
            # take locations from here, to generate the geojson down below if new draft
            submodels.create_locations(deal, meta_activity.loc_groups, do_save, rev1)
            submodels.create_contracts(deal, meta_activity.con_groups, do_save, rev1)
            submodels.create_data_sources(deal, meta_activity.ds_groups, do_save, rev1)

        deal.status, deal.draft_status = calculate_new_stati(deal, new_status)

        if do_save:
            # save the actual model
            # if: there is not a current_model
            # or: there is a current model but it's a draft
            # or: the new status is Live, Updated or Deleted
            deal.save()
        elif new_status == 1:
            deal.geojson = deal._combine_geojson()
        Version.create_from_obj(deal, rev1.id)

        if not do_save:
            # FIXME: it seems like this is not happening... might have to investigate
            # otherwise update the draft_status of the current_model
            Deal.objects.filter(pk=deal.pk).update(draft_status=deal.draft_status)
