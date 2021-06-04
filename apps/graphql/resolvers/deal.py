import base64
import os
from typing import Any

from django.core.files.storage import DefaultStorage
from django.utils import timezone
from django.utils.html import linebreaks
from django_comments.models import Comment
from graphql import GraphQLResolveInfo, GraphQLError

from apps.graphql.tools import get_fields, parse_filters
from apps.landmatrix.models import Deal, Country
from apps.landmatrix.models.deal import DealVersion, DealWorkflowInfo
from apps.landmatrix.models.versions import Revision
from apps.utils import qs_values_to_dict


# def map_raw_sql():
#     sql = """
#     select json_build_object(
#     'id',ld.id,
#     'deal_size',ld.deal_size,
#     'country',(SELECT json_build_object('id',c.id,'name',c.name) from landmatrix_country c where c.id=ld.country_id),
#     'locations',(
#         SELECT json_agg(locs)
#         from landmatrix_location locs where locs.deal_id=ld.id
#         )
#     ) from landmatrix_deal ld
#     where ld.id=6869;
#     """


def resolve_deal(_, info: GraphQLResolveInfo, id, version=None, subset="PUBLIC"):
    fields = get_fields(info, recursive=True, exclude=["__typename"])

    add_versions = False
    add_workflowinfos = False
    add_comments = False
    filtered_fields = []
    for field in fields:
        if "versions" in field:
            add_versions = True
        elif "workflowinfos" in field:
            add_workflowinfos = True
        elif "comments" in field:
            add_comments = True
        else:
            filtered_fields += [field]

    if version:
        rev = Revision.objects.get(id=version)
        deal = rev.dealversion_set.get().fields
    else:
        visible_deals = Deal.objects.visible(
            info.context["request"].user, subset
        ).filter(id=id)
        if not visible_deals:
            return

        deal = qs_values_to_dict(
            visible_deals,
            filtered_fields,
            ["top_investors", "parent_companies"],
        )[0]

    if deal.get("locations") is None:
        deal["locations"] = []
    if deal.get("contracts") is None:
        deal["contracts"] = []
    if deal.get("datasources") is None:
        deal["datasources"] = []

    if add_versions:
        deal["versions"] = [
            dv.to_dict() for dv in DealVersion.objects.filter(object_id=id)
        ]
    if add_workflowinfos:
        deal["workflowinfos"] = [
            dwi.to_dict()
            for dwi in DealWorkflowInfo.objects.filter(deal_id=id).order_by(
                "-timestamp"
            )
        ]
    if add_comments:
        deal["comments"] = [
            {
                "id": comm.id,
                "comment": linebreaks(comm.comment),
                "submit_date": comm.submit_date,
                "userinfo": comm._get_userinfo(),
            }
            for comm in Comment.objects.filter(content_type_id=125, object_pk=id)
        ]
    return deal


def resolve_deals(
    obj: Any,
    info: GraphQLResolveInfo,
    sort="id",
    limit=20,
    subset="PUBLIC",
    filters=None,
):
    qs = Deal.objects.visible(
        user=info.context["request"].user, subset=subset
    ).order_by(sort)

    if filters:
        qs = qs.filter(parse_filters(filters))

    fields = get_fields(info, recursive=True, exclude=["__typename"])

    if any(["involvements" in field for field in fields]):
        raise GraphQLError(
            "Querying involvements via multiple operating companies is too"
            " resource intensive. Please use single investor queries for this."
        )

    if limit != 0:
        qs = qs[:limit]

    return qs_values_to_dict(
        qs,
        fields,
        ["top_investors", "parent_companies"],
    )


def _resolve_field_dict_fetch(field_dict, revision):
    field_dict["datasources_count"] = revision.version_set.filter(
        content_type__model="datasource"
    ).count()

    return field_dict


def resolve_dealversions(
    obj, info: GraphQLResolveInfo, filters=None, country_id=None, region_id=None
):
    qs = DealVersion.objects.all()

    if filters:
        qs = qs.filter(parse_filters(filters))

    if country_id:
        qs = qs.filter(serialized_data__0__fields__country=country_id)

    if region_id:
        country_ids = list(
            Country.objects.filter(fk_region_id=region_id).values_list("id", flat=True)
        )
        qs = qs.filter(serialized_data__0__fields__country__in=country_ids)

    return [dv.to_dict() for dv in qs]


storage = DefaultStorage()


def resolve_upload_datasource_file(_, info, filename, payload) -> str:
    _, data = payload.split(",")
    dec = base64.b64decode(data)
    fname = storage.get_available_name(f"uploads/{filename}")
    with open(os.path.join(storage.base_location, fname), "wb+") as f:
        f.write(dec)
    return fname


def resolve_change_deal_status(_, info, id, transition) -> int:
    deal = Deal.objects.get(id=id)

    status = Deal.STATUS_DRAFT
    if transition == "TO_DRAFT":
        draft_status = Deal.DRAFT_STATUS_DRAFT
    elif transition == "TO_REVIEW":
        draft_status = Deal.DRAFT_STATUS_REVIEW
    elif transition == "TO_ACTIVATION":
        draft_status = Deal.DRAFT_STATUS_ACTIVATION
    elif transition == "ACTIVATE":
        status = (
            Deal.STATUS_LIVE
            if deal.status == Deal.STATUS_DRAFT
            else Deal.STATUS_UPDATED
        )
        draft_status = None
    else:
        raise GraphQLError(f"Invalid transition {transition}")

    # Note: Assuming here, that we're always operating on the latest Version object if we're already live.
    if deal.status != Deal.STATUS_DRAFT:
        Deal.objects.filter(id=id).update(draft_status=draft_status)
        deal = (
            DealVersion.objects.filter(object_id=deal.id)
            .order_by("-id")[0]
            .retrieve_object()
        )

    status_str = dict(Deal.STATUS_CHOICES).get(status, "")
    draft_status_str = dict(Deal.DRAFT_STATUS_CHOICES).get(draft_status, "")
    # TODO: assure neccessary rights concerning user and updating the deal
    # TODO: stupid old ubuntu
    user = info.context["request"].user
    if user and user.is_authenticated:
        deal.draft_status = draft_status
        deal.status = status
        if not draft_status:
            deal.save()
        rev = deal.save_revision(
            date_created=timezone.now(),
            user=user,
            comment=f"Changed Status: {status_str} {draft_status_str}",
        )
        return rev.id
    return -1


def resolve_deal_edit(_, info, id, version=None, payload: dict = None) -> dict:
    user = info.context["request"].user
    # print(f"id: {id}")
    # print(f"version: {version}")
    # print(f"payload: {payload}")

    if not user.is_authenticated:

        raise GraphQLError("not authorized")

    # this is a new Deal
    if id == -1:
        deal = Deal()
        deal.update_from_dict(payload)
        deal.status = deal.draft_status = Deal.DRAFT_STATUS_DRAFT
        deal.save()
        rev = deal.save_revision(
            date_created=timezone.now(),
            user=info.context["request"].user,
        )
        return {"dealId": deal.id, "dealVersion": rev.id}

    # TODO make sure user is allowed to edit this deal.
    deal = Deal.objects.get(id=id)

    # this is a live Deal for which we create a new Version
    if not version:
        deal.update_from_dict(payload)
        deal.draft_status = Deal.DRAFT_STATUS_DRAFT
        rev = deal.save_revision(
            date_created=timezone.now(), user=info.context["request"].user
        )
        Deal.objects.filter(id=id).update(draft_status=Deal.DRAFT_STATUS_DRAFT)
    # we update the existing version.
    else:
        rev = Revision.objects.get(id=version)
        deal_version = DealVersion.objects.get(revision=rev)
        deal.update_from_dict(payload)
        deal_version.update_from_obj(deal)

    return {"dealId": id, "dealVersion": rev.id}
