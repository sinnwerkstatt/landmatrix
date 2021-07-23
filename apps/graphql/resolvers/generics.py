from django.utils import timezone
from graphql import GraphQLError

from apps.graphql.resolvers.user_utils import get_user_role, send_comment_to_user
from apps.landmatrix.models.deal import DealWorkflowInfo, Deal, DealVersion
from apps.landmatrix.models.gndinvestor import (
    InvestorWorkflowInfo,
    Investor,
    InvestorVersion,
)
from apps.landmatrix.models.versions import Revision, Version


def add_workflow_info(otype, obj, obj_version, **kwargs):
    if otype == "deal":
        wfi = DealWorkflowInfo.objects.create(
            deal=obj, object_version=obj_version, **kwargs
        )
    else:
        wfi = InvestorWorkflowInfo.objects.create(
            investor=obj, investor_version=obj_version, **kwargs
        )
    return wfi


def get_object_version(otype, version_id):
    if otype == "deal":
        return DealVersion.objects.get(revision_id=version_id)
    if otype == "investor":
        return InvestorVersion.objects.get(revision_id=version_id)


def add_object_comment(
    otype, user, obj_id, obj_version_id: int, comment: str, to_user_id=None
) -> None:
    role = get_user_role(user)
    if not role:
        raise GraphQLError("not allowed")

    obj = (Deal if otype == "deal" else Investor).objects.get(id=obj_id)
    object_version = None
    draft_status = None

    if obj_version_id:
        object_version = (
            DealVersion if otype == "deal" else InvestorVersion
        ).objects.get(revision_id=obj_version_id)
        object_version_object = object_version.retrieve_object()
        draft_status = object_version_object.draft_status

    add_workflow_info(
        otype,
        obj,
        object_version,
        from_user=user,
        to_user_id=to_user_id,
        draft_status_before=draft_status,
        draft_status_after=draft_status,
        comment=comment,
    )

    if to_user_id:
        send_comment_to_user(
            obj,
            comment,
            user,
            to_user_id,
            obj_version_id,
        )


def change_obj_status(
    otype,
    user,
    obj_id,
    obj_version_id: int,
    transition: str,
    comment: str = None,
    to_user_id: int = None,
    fully_updated: bool = False,  # only relevant on "TO_REVIEW"
) -> list:

    role = get_user_role(user)
    if role not in ["ADMINISTRATOR", "EDITOR", "REPORTER"]:
        raise GraphQLError("not allowed")
    Object = Deal if otype == "deal" else Investor
    obj = Object.objects.get(id=obj_id)
    rev = Revision.objects.get(id=obj_version_id)
    object_version = (DealVersion if otype == "deal" else InvestorVersion).objects.get(
        revision_id=obj_version_id
    )

    object_version_object = object_version.retrieve_object()
    old_draft_status = object_version_object.draft_status

    if transition == "TO_REVIEW":
        if not (rev.user == user or role in ["ADMINISTRATOR", "EDITOR"]):
            raise GraphQLError("not authorized")

        draft_status = Deal.DRAFT_STATUS_REVIEW
        object_version_object.draft_status = draft_status
        if otype == "deal":
            object_version_object.fully_updated = fully_updated
        object_version.update_from_obj(object_version_object).save()
        Object.objects.filter(id=id).update(draft_status=draft_status)

    elif transition == "TO_ACTIVATION":
        if role not in ["ADMINISTRATOR", "EDITOR"]:
            raise GraphQLError("not authorized")
        draft_status = Deal.DRAFT_STATUS_ACTIVATION
        object_version_object.draft_status = draft_status
        object_version.update_from_obj(object_version_object).save()
        Object.objects.filter(id=id).update(draft_status=draft_status)
    elif transition == "ACTIVATE":
        if role != "ADMINISTRATOR":
            raise GraphQLError("not allowed")
        draft_status = None
        object_version_object.status = (
            Deal.STATUS_LIVE if obj.status == Deal.STATUS_DRAFT else Deal.STATUS_UPDATED
        )
        object_version_object.draft_status = draft_status
        object_version_object.current_draft = None
        object_version_object.save()
        object_version.update_from_obj(object_version_object).save()
    elif transition == "TO_DRAFT":
        if role not in ["ADMINISTRATOR", "EDITOR"]:
            raise GraphQLError("not authorized")
        draft_status = obj.draft_status = Deal.DRAFT_STATUS_DRAFT
        rev = Revision.objects.create(date_created=timezone.now(), user_id=to_user_id)
        Version.create_from_obj(obj, revision_id=rev.id)
        Object.objects.filter(id=id).update(draft_status=draft_status)
    else:
        raise GraphQLError(f"unknown transition {transition}")

    add_workflow_info(
        otype,
        obj,
        object_version,
        from_user=user,
        to_user_id=to_user_id,
        draft_status_before=old_draft_status,
        draft_status_after=draft_status,
        comment=comment,
    )
    if to_user_id:
        send_comment_to_user(obj, comment, user, to_user_id, obj_version_id)

    return [obj.id, rev.id]
