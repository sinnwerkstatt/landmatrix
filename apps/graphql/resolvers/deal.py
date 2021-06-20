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
from apps.landmatrix.models.versions import Revision, Version
from apps.utils import qs_values_to_dict
from .user_utils import send_comment_to_user, get_user_role

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
    user = info.context["request"].user
    role = get_user_role(user)
    if role not in ["ADMINISTRATOR", "EDITOR", "REPORTER"]:
        raise GraphQLError("not allowed")

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
        send_comment_to_user(deal, comment, user, to_user_id, version)

    return {"dealId": deal.id, "dealVersion": version}


def resolve_change_deal_status(
    _,
    info,
    id: int,
    version: int,
    transition: str,
    comment: str = None,
    to_user_id: int = None,
) -> dict:
    user = info.context["request"].user
    role = get_user_role(user)
    if not user.is_authenticated:
        raise GraphQLError("not authorized")

    deal = Deal.objects.get(id=id)
    rev = Revision.objects.get(id=version)
    deal_version = DealVersion.objects.get(revision=rev)

    deal_v_obj = deal_version.retrieve_object()
    old_draft_status = deal_v_obj.draft_status

    if transition == "TO_REVIEW":
        if not (
            deal_version.revision.user == user or role in ["ADMINISTRATOR", "EDITOR"]
        ):
            raise GraphQLError("not authorized")
        draft_status = Deal.DRAFT_STATUS_REVIEW
        deal_v_obj.draft_status = draft_status
        deal_version.update_from_obj(deal_v_obj).save()
        Deal.objects.filter(id=id).update(draft_status=draft_status)
    elif transition == "TO_ACTIVATION":
        if role not in ["ADMINISTRATOR", "EDITOR"]:
            raise GraphQLError("not authorized")
        draft_status = Deal.DRAFT_STATUS_ACTIVATION
        deal_v_obj.draft_status = draft_status
        deal_version.update_from_obj(deal_v_obj).save()
        Deal.objects.filter(id=id).update(draft_status=draft_status)
    elif transition == "ACTIVATE":
        if role != "ADMINISTRATOR":
            raise GraphQLError("not allowed")
        draft_status = None
        deal_v_obj.status = (
            Deal.STATUS_LIVE
            if deal.status == Deal.STATUS_DRAFT
            else Deal.STATUS_UPDATED
        )
        deal_v_obj.draft_status = draft_status
        deal_v_obj.save()
        deal_version.update_from_obj(deal_v_obj).save()
    elif transition == "TO_DRAFT":
        if role not in ["ADMINISTRATOR", "EDITOR"]:
            raise GraphQLError("not authorized")
        draft_status = Deal.DRAFT_STATUS_DRAFT
        deal_v_obj.draft_status = draft_status
        rev = deal_v_obj.save_revision(date_created=timezone.now(), user_id=to_user_id)
        Deal.objects.filter(id=id).update(draft_status=draft_status)
    else:
        raise GraphQLError(f"unknown transition {transition}")

    DealWorkflowInfo.objects.create(
        deal=deal,
        deal_version=deal_version,
        from_user=user,
        to_user_id=to_user_id,
        draft_status_before=old_draft_status,
        draft_status_after=draft_status,
        comment=comment,
    )

    if to_user_id:
        send_comment_to_user(deal, comment, user, to_user_id, version)

    return {"dealId": deal.id, "dealVersion": rev.id}


def resolve_deal_edit(_, info, id, version=None, payload: dict = None) -> dict:
    user = info.context["request"].user
    role = get_user_role(user)
    if not role:
        raise GraphQLError("not authorized")

    # this is a new Deal
    if id == -1:
        deal = Deal()
        deal.update_from_dict(payload)
        deal.recalculate_fields()
        deal.modified_at = timezone.now()
        deal.status = deal.draft_status = Deal.DRAFT_STATUS_DRAFT
        deal.save()
        rev = Revision.objects.create(
            date_created=timezone.now(), user=user, comment=""
        )
        deal_version = Version.create_from_obj(deal, revision_id=rev.id)
        DealWorkflowInfo.objects.create(
            deal=deal,
            deal_version=deal_version,
            from_user=user,
            draft_status_after=deal.draft_status,
        )

        return {"dealId": deal.id, "dealVersion": rev.id}

    # TODO make sure user is allowed to edit this deal.

    deal = Deal.objects.get(id=id)
    deal.update_from_dict(payload)
    deal.recalculate_fields()
    deal.modified_at = timezone.now()

    # this is a live Deal for which we create a new Version
    if not version:
        deal.draft_status = Deal.DRAFT_STATUS_DRAFT
        rev = deal.save_revision(date_created=timezone.now(), user=user)
        Deal.objects.filter(id=id).update(draft_status=Deal.DRAFT_STATUS_DRAFT)

        deal_version = DealVersion.objects.get(revision=rev)
        deal_v_obj = deal_version.retrieve_object()
        DealWorkflowInfo.objects.create(
            deal=deal,
            deal_version=deal_version,
            from_user=user,
            draft_status_before=None,
            draft_status_after=deal_v_obj.draft_status,
        )

    # we update the existing version.
    else:
        rev = Revision.objects.get(id=version)
        deal_version = DealVersion.objects.get(revision=rev)
        if not (
            deal_version.revision.user == user or role in ["ADMINISTRATOR", "EDITOR"]
        ):
            raise GraphQLError("not authorized")

        deal_version.update_from_obj(deal)
        if deal.draft_status in [
            Deal.DRAFT_STATUS_REVIEW,
            Deal.DRAFT_STATUS_ACTIVATION,
        ]:
            oldstatus = deal.draft_status
            rev = Revision.objects.create(
                date_created=timezone.now(), user=user, comment=""
            )
            tmp_deal = deal_version.retrieve_object()
            tmp_deal.draft_status = Deal.DRAFT_STATUS_DRAFT
            dv = Version.create_from_obj(tmp_deal, revision_id=rev.id)
            DealWorkflowInfo.objects.create(
                deal=deal,
                deal_version=dv,
                from_user=user,
                draft_status_before=oldstatus,
                draft_status_after=Deal.DRAFT_STATUS_DRAFT,
            )
        else:
            deal_version.save()
            if deal.status == Deal.STATUS_DRAFT:
                deal.save()

    return {"dealId": id, "dealVersion": rev.id}


def resolve_deal_delete(_, info, id, version=None, comment=None) -> bool:
    # TODO make sure user is allowed to edit this deal.
    user = info.context["request"].user
    role = get_user_role(user)
    if not role:
        raise GraphQLError("not authorized")

    deal = Deal.objects.get(id=id)
    # if it's just a draft,
    if version:
        rev = Revision.objects.get(id=version)
        deal_version = DealVersion.objects.get(revision=rev)
        if not (
            deal_version.revision.user == user or role in ["ADMINISTRATOR", "EDITOR"]
        ):
            raise GraphQLError("not authorized")
        deal_v_obj = deal_version.retrieve_object()
        old_draft_status = deal_v_obj.draft_status
        deal_version.delete()
        DealWorkflowInfo.objects.create(
            deal=deal,
            from_user=user,
            draft_status_before=old_draft_status,
            draft_status_after=deal.status == Deal.STATUS_DELETED,
            comment=comment,
        )
        if deal.versions.count() == 0 and deal.status == Deal.STATUS_DRAFT:
            Revision.objects.filter(dealversion__object_id=deal.id).delete()
            deal.delete()

    else:
        if role != "ADMINISTRATOR":
            raise GraphQLError("not authorized")
        deal.status = (
            Deal.STATUS_UPDATED
            if deal.status == Deal.STATUS_DELETED
            else Deal.STATUS_DELETED
        )
        deal.modified_at = timezone.now()
        deal.save()
        DealWorkflowInfo.objects.create(
            deal=deal,
            from_user=user,
            draft_status_before=(
                None
                if deal.status == Deal.STATUS_DELETED
                else Deal.DRAFT_STATUS_TO_DELETE
            ),
            draft_status_after=(
                Deal.DRAFT_STATUS_TO_DELETE
                if deal.status == Deal.STATUS_DELETED
                else None
            ),
            comment=comment,
        )
    return True


def resolve_set_confidential(
    _, info, id, confidential, version=None, reason=None, comment=None
) -> bool:
    user = info.context["request"].user
    role = get_user_role(user)
    if not role:
        raise GraphQLError("not authorized")

    if version:
        rev = Revision.objects.get(id=version)
        deal_version = DealVersion.objects.get(revision=rev)
        if not (
            deal_version.revision.user == user or role in ["ADMINISTRATOR", "EDITOR"]
        ):
            raise GraphQLError("not authorized")
        deal_v_obj = deal_version.retrieve_object()
        deal_v_obj.confidential = confidential
        deal_v_obj.confidential_reason = reason
        deal_v_obj.confidential_comment = comment
        deal_v_obj.modified_at = timezone.now()
        deal_version.update_from_obj(deal_v_obj).save()

    else:
        if role != "ADMINISTRATOR":
            raise GraphQLError("not authorized")
        deal = Deal.objects.get(id=id)
        deal.confidential = confidential
        deal.confidential_reason = reason
        deal.confidential_comment = comment
        deal.modified_at = timezone.now()
        deal.save()
    return True
