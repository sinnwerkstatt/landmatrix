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
from .generics import (
    add_object_comment,
    change_object_status,
    object_edit,
    object_delete,
)
from .user_utils import get_user_role

storage = DefaultStorage()


def resolve_deal(_, info: GraphQLResolveInfo, id, version=None, subset="PUBLIC"):
    user = info.context["request"].user
    fields = get_fields(info, recursive=True, exclude=["__typename"])

    role = get_user_role(user)

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
        elif "revision" in field:
            pass  # ignore this field on "Deal", just set it on DealVersion
        else:
            filtered_fields += [field]

    if version:
        try:
            rev = Revision.objects.get(id=version)
        except Revision.DoesNotExist:
            return
        try:
            deal = rev.dealversion_set.get().fields
        except DealVersion.DoesNotExist:
            return
        if not (rev.user == user or role in ["ADMINISTRATOR", "EDITOR"]):
            raise GraphQLError("not authorized")
        deal["created_at"] = rev.date_created
        deal["revision"] = rev
    else:
        visible_deals = Deal.objects.visible(user, subset).filter(id=id)
        if not visible_deals:
            raise GraphQLError("deal not found")

        deal = qs_values_to_dict(
            visible_deals,
            filtered_fields,
            ["top_investors", "parent_companies", "workflowinfos"],
        )[0]

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

    if deal.get("locations") is None:
        deal["locations"] = []
    if deal.get("contracts") is None:
        deal["contracts"] = []
    if deal.get("datasources") is None:
        deal["datasources"] = []

    return deal


def resolve_deals(
    _,
    info: GraphQLResolveInfo,
    sort="id",
    limit=20,
    subset="PUBLIC",
    filters=None,
):
    user = info.context["request"].user
    qs = Deal.objects.visible(user=user, subset=subset).order_by(sort)

    fields = get_fields(info, recursive=True, exclude=["__typename"])
    if any(["involvements" in field for field in fields]):
        raise GraphQLError(
            "Querying involvements via multiple operating companies is too"
            " resource intensive. Please use single investor queries for this."
        )

    qs = qs.filter(parse_filters(filters)) if filters else qs

    qs = qs[:limit] if limit != 0 else qs

    return qs_values_to_dict(
        qs,
        fields,
        ["top_investors", "parent_companies", "workflowinfos"],
    )


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


def resolve_upload_datasource_file(_, info, filename, payload) -> str:
    user = info.context["request"].user
    if not user.is_authenticated:
        raise GraphQLError("not authorized")

    _, data = payload.split(",")
    dec = base64.b64decode(data)
    fname = storage.get_available_name(f"uploads/{filename}")
    with open(os.path.join(storage.base_location, fname), "wb+") as f:
        f.write(dec)
    return fname


def resolve_add_deal_comment(
    _, info, id: int, version: int, comment: str, to_user_id=None
) -> dict:
    add_object_comment(
        "deal", info.context["request"].user, id, version, comment, to_user_id
    )

    return {"dealId": id, "dealVersion": version}


def resolve_change_deal_status(
    _,
    info,
    id: int,
    version: int,
    transition: str,
    comment: str = None,
    to_user_id: int = None,
    fully_updated: bool = False,  # only relevant on "TO_REVIEW"
) -> dict:
    dealId, dealVersion = change_object_status(
        otype="deal",
        user=info.context["request"].user,
        obj_id=id,
        obj_version_id=version,
        transition=transition,
        comment=comment,
        to_user_id=to_user_id,
        fully_updated=fully_updated,
    )
    return {"dealId": dealId, "dealVersion": dealVersion}


def resolve_deal_edit(_, info, id, version=None, payload: dict = None) -> dict:
    dealId, dealVersion = object_edit(
        otype="deal",
        user=info.context["request"].user,
        obj_id=id,
        obj_version_id=version,
        payload=payload,
    )
    return {"dealId": dealId, "dealVersion": dealVersion}


def resolve_deal_delete(
    _, info, id: int, version: int = None, comment: str = None
) -> bool:
    return object_delete(
        otype="deal",
        user=info.context["request"].user,
        obj_id=id,
        obj_version_id=version,
        comment=comment,
    )


def resolve_set_confidential(
    _, info, id, confidential, version=None, reason=None, comment=None
) -> bool:
    user = info.context["request"].user
    role = get_user_role(user)
    if not role:
        raise GraphQLError("not authorized")

    if version:
        deal_version = DealVersion.objects.get(revision_id=version)
        if not (
            deal_version.revision.user == user or role in ["ADMINISTRATOR", "EDITOR"]
        ):
            raise GraphQLError("not authorized")
        deal_v_obj = deal_version.retrieve_object()
        deal_v_obj.confidential = confidential
        deal_v_obj.confidential_reason = reason
        deal_v_obj.confidential_comment = comment
        deal_v_obj.modified_at = timezone.now()
        deal_v_obj.modified_by = user
        deal_version.update_from_obj(deal_v_obj).save()

    else:
        if role != "ADMINISTRATOR":
            raise GraphQLError("not authorized")
        deal = Deal.objects.get(id=id)
        deal.confidential = confidential
        deal.confidential_reason = reason
        deal.confidential_comment = comment
        deal.modified_at = timezone.now()
        deal.modified_by = user
        deal.save()
    return True
