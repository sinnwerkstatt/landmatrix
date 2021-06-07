import base64
import os
from typing import Any

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.storage import DefaultStorage
from django.utils import timezone
from django.utils.html import linebreaks
from django.utils.translation import ugettext
from django_comments.models import Comment
from graphql import GraphQLResolveInfo, GraphQLError
from wagtail.core.models import Site

from apps.graphql.tools import get_fields, parse_filters
from apps.landmatrix.models import Deal, Country
from apps.landmatrix.models.deal import DealVersion, DealWorkflowInfo
from apps.landmatrix.models.versions import Revision, Version
from apps.utils import qs_values_to_dict

User = get_user_model()


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
    user = info.context["request"].user
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
        # if not user.is_authenticated:
        #     return
        rev = Revision.objects.get(id=version)
        deal = rev.dealversion_set.get().fields
    else:
        visible_deals = Deal.objects.visible(user, subset).filter(id=id)
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


def resolve_add_deal_comment(
    _, info, id: int, version: int, comment: str, to_user_id=None
) -> dict:
    user = info.context["request"].user
    if not user.is_authenticated:
        raise GraphQLError("not authorized")

    deal = Deal.objects.get(id=id)
    deal_version = None
    draft_status = None
    if version:
        rev = Revision.objects.get(id=version)
        deal_version = DealVersion.objects.get(revision=rev)
        deal_v_obj = deal_version.retrieve_object()
        draft_status = deal_v_obj.draft_status

    DealWorkflowInfo.objects.create(
        deal=deal,
        deal_version=deal_version,
        from_user=user,
        to_user_id=to_user_id,
        draft_status_before=draft_status,
        draft_status_after=draft_status,
        comment=comment,
    )

    if to_user_id:
        reciever = User.objects.get(id=to_user_id)
        subject = "[Landmatrix] " + ugettext("New comment")
        print(user.__dict__)
        message = ugettext(
            f"{user.get_full_name()} has addressed you in a comment on deal {deal.id}:"
        )
        message += "\n\n" + comment

        site = Site.objects.get(is_default_site=True)
        url = f"http{'s' if site.port == 444 else ''}://{site.hostname}"
        if site.port not in [80, 443]:
            url += f":{site.port}"
        url += f"/deal/{deal.id}"
        if version:
            url += f"/{version}"
        message += "\n\n" + ugettext(f"Please review at {url}")

        reciever.email_user(subject, message, from_email=settings.DEFAULT_FROM_EMAIL)

    return {"dealId": deal.id, "dealVersion": version}


def resolve_change_deal_status(
    _, info, id: int, version: int, transition: str = ""
) -> dict:
    user = info.context["request"].user
    if not user.is_authenticated:
        raise GraphQLError("not authorized")

    deal = Deal.objects.get(id=id)
    rev = Revision.objects.get(id=version)
    deal_version = DealVersion.objects.get(revision=rev)

    deal_v_obj = deal_version.retrieve_object()
    old_draft_status = deal_v_obj.draft_status

    # TODO: assure neccessary rights concerning user and updating the deal
    if transition == "ACTIVATE":
        draft_status = None
        deal_v_obj.status = (
            Deal.STATUS_LIVE
            if deal.status == Deal.STATUS_DRAFT
            else Deal.STATUS_UPDATED
        )
        deal_v_obj.draft_status = draft_status
        deal_v_obj.save()
        deal_version.update_from_obj(deal_v_obj)
        deal_version.save()

    else:
        draft_status = {
            "TO_DRAFT": Deal.DRAFT_STATUS_DRAFT,
            "TO_REVIEW": Deal.DRAFT_STATUS_REVIEW,
            "TO_ACTIVATION": Deal.DRAFT_STATUS_ACTIVATION,
        }[transition]
        deal_v_obj.draft_status = draft_status
        deal_version.update_from_obj(deal_v_obj)
        deal_version.save()

        Deal.objects.filter(id=id).update(draft_status=draft_status)

    DealWorkflowInfo.objects.create(
        deal=deal,
        deal_version=deal_version,
        from_user=user,
        # to_user
        draft_status_before=old_draft_status,
        draft_status_after=draft_status,
        # comment
    )
    return {"dealId": deal.id, "dealVersion": rev.id}


def resolve_deal_edit(_, info, id, version=None, payload: dict = None) -> dict:
    user = info.context["request"].user
    if not user.is_authenticated:
        raise GraphQLError("not authorized")

    # this is a new Deal
    if id == -1:
        deal = Deal()
        deal.update_from_dict(payload)
        deal.recalculate_fields()
        deal.status = deal.draft_status = Deal.DRAFT_STATUS_DRAFT
        deal.save()
        rev = Revision.objects.create(
            date_created=timezone.now(), user=user, comment=""
        )
        Version.create_from_obj(deal, revision_id=rev.id)
        return {"dealId": deal.id, "dealVersion": rev.id}

    # TODO make sure user is allowed to edit this deal.

    deal = Deal.objects.get(id=id)
    deal.update_from_dict(payload)
    deal.recalculate_fields()

    # this is a live Deal for which we create a new Version
    if not version:
        deal.draft_status = Deal.DRAFT_STATUS_DRAFT
        rev = deal.save_revision(date_created=timezone.now(), user=user)
        Deal.objects.filter(id=id).update(draft_status=Deal.DRAFT_STATUS_DRAFT)
    # we update the existing version.
    else:
        rev = Revision.objects.get(id=version)
        deal_version = DealVersion.objects.get(revision=rev)
        deal_version.update_from_obj(deal)
        deal_version.save()

    return {"dealId": id, "dealVersion": rev.id}
