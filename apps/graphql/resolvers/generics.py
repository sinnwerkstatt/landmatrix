from typing import List

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


def add_workflow_info(otype, obj, obj_version=None, **kwargs):
    if otype == "deal":
        wfi = DealWorkflowInfo.objects.create(
            deal=obj, deal_version=obj_version, **kwargs
        )
    else:
        wfi = InvestorWorkflowInfo.objects.create(
            investor=obj, investor_version=obj_version, **kwargs
        )
    return wfi


def add_object_comment(
    otype, user, obj_id, obj_version_id: int, comment: str, to_user_id=None
) -> None:
    role = get_user_role(user)
    if not role:
        raise GraphQLError("not allowed")

    obj = (Deal if otype == "deal" else Investor).objects.get(id=obj_id)
    obj_version = None
    draft_status = None

    if obj_version_id:
        obj_version = (DealVersion if otype == "deal" else InvestorVersion).objects.get(
            revision_id=obj_version_id
        )
        draft_status = obj_version.retrieve_object().draft_status

    add_workflow_info(
        otype,
        obj,
        obj_version,
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


def change_object_status(
    otype,
    user,
    obj_id,
    obj_version_id: int,
    transition: str,
    comment: str = None,
    to_user_id: int = None,
    fully_updated: bool = False,  # only relevant on "TO_REVIEW"
) -> List[int]:

    role = get_user_role(user)
    if role not in ["ADMINISTRATOR", "EDITOR", "REPORTER"]:
        raise GraphQLError("not allowed")
    Object = Deal if otype == "deal" else Investor
    obj = Object.objects.get(id=obj_id)
    rev = Revision.objects.get(id=obj_version_id)
    obj_version = (DealVersion if otype == "deal" else InvestorVersion).objects.get(
        revision_id=obj_version_id
    )

    obj_version_object = obj_version.retrieve_object()
    old_draft_status = obj_version_object.draft_status

    if transition == "TO_REVIEW":
        if not (rev.user == user or role in ["ADMINISTRATOR", "EDITOR"]):
            raise GraphQLError("not authorized")

        draft_status = Deal.DRAFT_STATUS_REVIEW
        obj_version_object.draft_status = draft_status
        if otype == "deal":
            obj_version_object.fully_updated = fully_updated
        obj_version.update_from_obj(obj_version_object).save()
        Object.objects.filter(id=id).update(draft_status=draft_status)

    elif transition == "TO_ACTIVATION":
        if role not in ["ADMINISTRATOR", "EDITOR"]:
            raise GraphQLError("not authorized")
        draft_status = Deal.DRAFT_STATUS_ACTIVATION
        obj_version_object.draft_status = draft_status
        obj_version.update_from_obj(obj_version_object).save()
        Object.objects.filter(id=id).update(draft_status=draft_status)
    elif transition == "ACTIVATE":
        if role != "ADMINISTRATOR":
            raise GraphQLError("not allowed")
        draft_status = None
        obj_version_object.status = (
            Deal.STATUS_LIVE if obj.status == Deal.STATUS_DRAFT else Deal.STATUS_UPDATED
        )
        obj_version_object.draft_status = draft_status
        obj_version_object.current_draft = None
        obj_version_object.save()
        obj_version.update_from_obj(obj_version_object).save()
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
        obj_version,
        from_user=user,
        to_user_id=to_user_id,
        draft_status_before=old_draft_status,
        draft_status_after=draft_status,
        comment=comment,
    )
    if to_user_id:
        send_comment_to_user(obj, comment, user, to_user_id, obj_version_id)

    return [obj.id, rev.id]


def object_edit(
    otype, user, obj_id, obj_version_id: int, payload: dict = None
) -> List[int]:

    role = get_user_role(user)
    if not role:
        raise GraphQLError("not authorized")

    Object = Deal if otype == "deal" else Investor

    # this is a new Object
    if id == -1:
        obj = Object()
        obj.update_from_dict(payload)
        obj.recalculate_fields()
        obj.created_by = user
        obj.modified_at = timezone.now()
        obj.modified_by = user
        obj.status = obj.draft_status = Deal.DRAFT_STATUS_DRAFT
        obj.save()

        rev = Revision.objects.create(date_created=timezone.now(), user=user)
        obj_version = Version.create_from_obj(obj, revision_id=rev.id)
        Object.objects.filter(id=obj.id).update(current_draft=obj_version)
        add_workflow_info(
            otype,
            obj,
            obj_version,
            from_user=user,
            draft_status_after=obj.draft_status,
        )

        return [obj.id, rev.id]

    obj = Object.objects.get(id=id)
    obj.update_from_dict(payload)
    obj.recalculate_fields()
    obj.modified_at = timezone.now()
    obj.modified_by = user

    # this is a live Object for which we create a new Version
    if not obj_version_id:
        obj.draft_status = Deal.DRAFT_STATUS_DRAFT
        if otype == "deal":
            obj.fully_updated = False
        rev = Revision.objects.create(date_created=timezone.now(), user=user)
        obj_version = Version.create_from_obj(obj, revision_id=rev.id)
        Object.objects.filter(id=id).update(
            draft_status=Deal.DRAFT_STATUS_DRAFT, current_draft=obj_version
        )

        add_workflow_info(
            otype,
            obj,
            obj_version,
            from_user=user,
            draft_status_before=None,
            draft_status_after=obj_version.retrieve_object().draft_status,
        )

    # we update the existing version.
    else:
        rev = Revision.objects.get(id=obj_version_id)
        obj_version = (DealVersion if otype == "deal" else InvestorVersion).objects.get(
            revision=rev
        )
        if not (
            obj_version.revision.user == user or role in ["ADMINISTRATOR", "EDITOR"]
        ):
            raise GraphQLError("not authorized")

        obj_version.update_from_obj(obj)
        if obj.draft_status in [
            Deal.DRAFT_STATUS_REVIEW,
            Deal.DRAFT_STATUS_ACTIVATION,
        ]:
            oldstatus = obj.draft_status
            rev = Revision.objects.create(date_created=timezone.now(), user=user)
            obj_version_object = obj_version.retrieve_object()
            obj_version_object.draft_status = Deal.DRAFT_STATUS_DRAFT
            dv = Version.create_from_obj(obj_version_object, revision_id=rev.id)

            add_workflow_info(
                otype,
                obj,
                dv,
                from_user=user,
                draft_status_before=oldstatus,
                draft_status_after=Deal.DRAFT_STATUS_DRAFT,
            )
        else:
            obj_version.save()
            if obj.status == Deal.STATUS_DRAFT:
                obj.save()

    return [obj_id, rev.id]


def object_delete(
    otype, user, obj_id, obj_version_id: int, comment: str = None
) -> bool:

    role = get_user_role(user)
    if not role:
        raise GraphQLError("not authorized")

    Object = Deal if otype == "deal" else Investor

    obj = Object.objects.get(id=id)

    # if it's just a draft,
    if obj_version_id:
        obj_version = (DealVersion if otype == "deal" else InvestorVersion).objects.get(
            revision_id=obj_version_id
        )
        if not (
            obj_version.revision.user == user or role in ["ADMINISTRATOR", "EDITOR"]
        ):
            raise GraphQLError("not authorized")
        obj_version_object = obj_version.retrieve_object()
        old_draft_status = obj_version_object.draft_status
        obj_version.delete()
        add_workflow_info(
            otype,
            obj,
            from_user=user,
            draft_status_before=old_draft_status,
            draft_status_after=Deal.STATUS_DELETED,
            comment=comment,
        )

        if (
            obj.versions.count()
            and not obj.versions.order_by("-id")[0].serialized_data[0]["fields"][
                "draft_status"
            ]
        ):
            # reset the Live version to "not having a draft" if we delete it.
            Object.objects.filter(id=id).update(draft_status=None)

        if obj.versions.count() == 0 and obj.status == Deal.STATUS_DRAFT:
            if otype == "deal":
                Revision.objects.filter(dealversion__object_id=obj.id).delete()
            else:
                Revision.objects.filter(investorversion__object_id=obj.id).delete()
            obj.delete()

    else:
        if role != "ADMINISTRATOR":
            raise GraphQLError("not authorized")
        obj.status = (
            Deal.STATUS_UPDATED
            if obj.status == Deal.STATUS_DELETED
            else Deal.STATUS_DELETED
        )
        obj.modified_at = timezone.now()
        obj.modified_by = user
        obj.save()
        add_workflow_info(
            otype,
            obj,
            from_user=user,
            draft_status_before=(
                None
                if obj.status == Deal.STATUS_DELETED
                else Deal.DRAFT_STATUS_TO_DELETE
            ),
            draft_status_after=(
                Deal.DRAFT_STATUS_TO_DELETE
                if obj.status == Deal.STATUS_DELETED
                else None
            ),
            comment=comment,
        )
    return True
