from typing import List, Union

from django.contrib.auth import get_user_model
from django.utils import timezone
from graphql import GraphQLError

from apps.graphql.resolvers.user_utils import get_user_role, send_comment_to_user
from apps.landmatrix.models.abstracts import DRAFT_STATUS, STATUS
from apps.landmatrix.models.deal import DealWorkflowInfo, Deal, DealVersion
from apps.landmatrix.models.gndinvestor import (
    InvestorWorkflowInfo,
    Investor,
    InvestorVersion,
)
from apps.utils import ecma262

# OType = Union[Literal["deal"], Literal["investor"]]
OType = str
User = get_user_model()


def add_workflow_info(
    otype: OType,
    obj: Union[Deal, Investor],
    obj_version: Union[DealVersion, InvestorVersion] = None,
    **kwargs,
) -> Union[DealWorkflowInfo, InvestorWorkflowInfo]:
    if otype == "deal":
        return DealWorkflowInfo.objects.create(
            deal=obj, deal_version=obj_version, **kwargs
        )
    else:
        return InvestorWorkflowInfo.objects.create(
            investor=obj, investor_version=obj_version, **kwargs
        )


def add_object_comment(
    otype: OType,
    user: User,
    obj_id: int,
    obj_version_id: int,
    comment: str,
    to_user_id=None,
) -> None:
    role = get_user_role(user)
    if not role:
        raise GraphQLError("not allowed")

    obj = (Deal if otype == "deal" else Investor).objects.get(id=obj_id)
    obj_version = None
    draft_status = None

    if obj_version_id:
        obj_version = (DealVersion if otype == "deal" else InvestorVersion).objects.get(
            id=obj_version_id
        )
        draft_status = obj_version.serialized_data["draft_status"]

    add_workflow_info(
        otype=otype,
        obj=obj,
        obj_version=obj_version,
        from_user=user,
        to_user_id=to_user_id,
        draft_status_before=draft_status,
        draft_status_after=draft_status,
        comment=comment,
    )

    if to_user_id:
        send_comment_to_user(obj, comment, user, to_user_id, obj_version_id)


def change_object_status(
    otype: OType,
    user: User,
    obj_id: int,
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
    ObjectVersion = DealVersion if otype == "deal" else InvestorVersion
    obj = Object.objects.get(id=obj_id)
    obj_version = ObjectVersion.objects.get(id=obj_version_id)

    old_draft_status = obj_version.serialized_data["draft_status"]

    if transition == "TO_REVIEW":
        if not (obj_version.created_by == user or role in ["ADMINISTRATOR", "EDITOR"]):
            raise GraphQLError("not authorized")

        draft_status = DRAFT_STATUS["REVIEW"]
        obj_version.serialized_data["draft_status"] = draft_status
        if otype == "deal":
            obj_version.serialized_data["fully_updated"] = fully_updated
            if fully_updated:
                obj_version.serialized_data["fully_updated_at"] = ecma262(
                    obj_version.created_at
                )
        obj_version.save()
        Object.objects.filter(id=obj_id).update(draft_status=draft_status)

    elif transition == "TO_ACTIVATION":
        if role not in ["ADMINISTRATOR", "EDITOR"]:
            raise GraphQLError("not authorized")
        draft_status = DRAFT_STATUS["ACTIVATION"]
        obj_version.serialized_data["draft_status"] = draft_status
        obj_version.save()
        Object.objects.filter(id=obj_id).update(draft_status=draft_status)
    elif transition == "ACTIVATE":
        if role != "ADMINISTRATOR":
            raise GraphQLError("not allowed")
        draft_status = None
        obj_version.serialized_data["status"] = (
            STATUS["LIVE"] if obj.status == STATUS["DRAFT"] else STATUS["UPDATED"]
        )
        obj_version.serialized_data["draft_status"] = draft_status
        obj_version.serialized_data["current_draft"] = None

        obj = Object.deserialize_from_version(obj_version)
        obj_version.save()
    elif transition == "TO_DRAFT":
        if role not in ["ADMINISTRATOR", "EDITOR"]:
            raise GraphQLError("not authorized")
        draft_status = DRAFT_STATUS["DRAFT"]

        obj_version.serialized_data["draft_status"] = draft_status
        obj_version.id = None
        obj_version.created_by_id = to_user_id
        obj_version.save()

        Object.objects.filter(id=obj_id).update(draft_status=draft_status)
    else:
        raise GraphQLError(f"unknown transition {transition}")

    add_workflow_info(
        otype=otype,
        obj=obj,
        obj_version=obj_version,
        from_user=user,
        to_user_id=to_user_id,
        draft_status_before=old_draft_status,
        draft_status_after=draft_status,
        comment=comment,
    )
    if to_user_id:
        send_comment_to_user(obj, comment, user, to_user_id, obj_version_id)

    return [obj.id, obj_version.id]


def object_edit(
    otype: OType,
    user: User,
    obj_id: int,
    obj_version_id: int = None,
    payload: dict = None,
) -> List[int]:
    role = get_user_role(user)
    if not role:
        raise GraphQLError("not authorized")
    Object = Deal if otype == "deal" else Investor
    ObjectVersion = DealVersion if otype == "deal" else InvestorVersion
    # this is a new Object
    if obj_id == -1:
        obj = Object()
        obj.update_from_dict(payload)
        obj.recalculate_fields()
        obj.created_by = user
        obj.modified_at = timezone.now()
        obj.modified_by = user
        obj.status = obj.draft_status = DRAFT_STATUS["DRAFT"]
        obj.save()

        obj_version = ObjectVersion.from_object(obj, created_by=user)
        Object.objects.filter(id=obj.id).update(current_draft=obj_version)
        add_workflow_info(
            otype=otype,
            obj=obj,
            obj_version=obj_version,
            from_user=user,
            draft_status_after=obj.draft_status,
        )

        return [obj.id, obj_version.id]
    obj = Object.objects.get(id=obj_id)
    obj.update_from_dict(payload)
    obj.recalculate_fields()
    obj.modified_at = timezone.now()
    obj.modified_by = user

    # this is a live Object for which we create a new Version
    if not obj_version_id:
        obj.draft_status = DRAFT_STATUS["DRAFT"]
        if otype == "deal":
            obj.fully_updated = False
        obj_version = ObjectVersion.from_object(obj, created_by=user)
        Object.objects.filter(id=obj_id).update(
            draft_status=DRAFT_STATUS["DRAFT"], current_draft=obj_version
        )

        add_workflow_info(
            otype=otype,
            obj=obj,
            obj_version=obj_version,
            from_user=user,
            draft_status_before=None,
            draft_status_after=DRAFT_STATUS["DRAFT"],
        )

    # we update the existing version.
    else:
        obj_version = (DealVersion if otype == "deal" else InvestorVersion).objects.get(
            id=obj_version_id
        )
        if not (obj_version.created_by == user or role in ["ADMINISTRATOR", "EDITOR"]):
            raise GraphQLError("not authorized")

        obj_version.serialized_data = obj.serialize_for_version()

        if obj.draft_status in [DRAFT_STATUS["REVIEW"], DRAFT_STATUS["ACTIVATION"]]:
            oldstatus = obj.draft_status

            obj_version.id = None
            obj_version.created_by = user
            obj_version.serialized_data["draft_status"] = DRAFT_STATUS["DRAFT"]
            obj_version.save()

            add_workflow_info(
                otype=otype,
                obj=obj,
                obj_version=obj_version,
                from_user=user,
                draft_status_before=oldstatus,
                draft_status_after=DRAFT_STATUS["DRAFT"],
            )
            Object.objects.filter(id=obj.id).update(current_draft=obj_version)
        else:
            obj_version.save()
            if obj.status == STATUS["DRAFT"]:
                obj.save()

    return [obj_id, obj_version.id]


def object_delete(
    otype: OType,
    user: User,
    obj_id: int,
    obj_version_id: int = None,
    comment: str = None,
) -> bool:
    role = get_user_role(user)
    if not role:
        raise GraphQLError("not authorized")

    Object = Deal if otype == "deal" else Investor
    obj = Object.objects.get(id=obj_id)

    # if it's just a draft,
    if obj_version_id:
        ObjectVersion = DealVersion if otype == "deal" else InvestorVersion
        obj_version = ObjectVersion.objects.get(id=obj_version_id)
        if not (obj_version.created_by == user or role in ["ADMINISTRATOR", "EDITOR"]):
            raise GraphQLError("not authorized")
        old_draft_status = obj_version.serialized_data["draft_status"]
        obj_version.delete()
        add_workflow_info(
            otype,
            obj,
            from_user=user,
            draft_status_before=old_draft_status,
            draft_status_after=STATUS["DELETED"],
            comment=comment,
        )

        if obj.versions.count() == 0 and obj.status == STATUS["DRAFT"]:
            Object.objects.get(id=obj.id).delete()

        if obj.versions.count() and not obj.versions[0].serialized_data["draft_status"]:
            # reset the Live version to "not having a draft" if we delete the draft.
            Object.objects.filter(id=obj_id).update(draft_status=None)

    else:
        if role != "ADMINISTRATOR":
            raise GraphQLError("not authorized")
        obj.status = (
            STATUS["UPDATED"] if obj.status == STATUS["DELETED"] else STATUS["DELETED"]
        )
        obj.modified_at = timezone.now()
        obj.modified_by = user
        obj.save()
        add_workflow_info(
            otype,
            obj,
            from_user=user,
            draft_status_before=(
                None if obj.status == STATUS["DELETED"] else DRAFT_STATUS["TO_DELETE"]
            ),
            draft_status_after=(
                DRAFT_STATUS["TO_DELETE"] if obj.status == STATUS["DELETED"] else None
            ),
            comment=comment,
        )
    return True
