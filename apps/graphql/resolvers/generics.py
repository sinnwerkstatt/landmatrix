from __future__ import annotations

from typing import Literal

from ariadne.graphql import GraphQLError
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils import timezone

from apps.graphql.resolvers.user_utils import get_user_role, send_comment_to_user
from apps.landmatrix.forms.deal import DealForm
from apps.landmatrix.forms.investor import InvestorForm
from apps.landmatrix.models.abstracts import DRAFT_STATUS, STATUS, WorkflowInfo
from apps.landmatrix.models.deal import Deal, DealVersion, DealWorkflowInfo
from apps.landmatrix.models.investor import (
    InvestorWorkflowInfo,
    Investor,
    InvestorVersion,
)
from apps.utils import ecma262

OType = Literal["deal", "investor"]
User = get_user_model()


def add_workflow_info(
    otype: OType,
    obj: Deal | Investor,
    obj_version: DealVersion | InvestorVersion = None,
    **kwargs,
) -> DealWorkflowInfo | InvestorWorkflowInfo:
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
) -> list[int]:
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

        # if there was a request for improvement workflowinfo, email the requester
        old_wfi: WorkflowInfo = obj.workflowinfos.last()
        if (
            old_wfi
            and old_wfi.draft_status_before in [2, 3]
            and old_wfi.draft_status_after == 1
            and old_wfi.to_user == user
        ):
            old_wfi.processed_by_received = True
            old_wfi.save()
            send_comment_to_user(obj, "", user, old_wfi.from_user_id, obj_version_id)

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

        # dirty hack for some investors with datasources == None
        if (
            "datasources" in obj_version.serialized_data
            and obj_version.serialized_data["datasources"] is None
        ):
            obj_version.serialized_data["datasources"] = []

        obj = Object.deserialize_from_version(obj_version)
        obj_version.save()
        # close remaining open feedback requests
        obj.workflowinfos.filter(
            Q(draft_status_before__in=[2, 3])
            & Q(draft_status_after=1)
            # TODO: https://git.sinntern.de/landmatrix/landmatrix/-/issues/404
            & (Q(from_user=user) | Q(to_user=user))
        ).update(processed_by_receiver=True)
    elif transition == "TO_DRAFT":
        if role not in ["ADMINISTRATOR", "EDITOR"]:
            raise GraphQLError("not authorized")
        draft_status = DRAFT_STATUS["DRAFT"]

        obj_version.serialized_data["draft_status"] = draft_status
        obj_version.id = None
        obj_version.created_by_id = to_user_id
        obj_version.save()

        Object.objects.filter(id=obj_id).update(
            draft_status=draft_status, current_draft=obj_version
        )
        # close remaining open feedback requests
        obj.workflowinfos.filter(
            Q(draft_status_before__in=[2, 3])
            & Q(draft_status_after=1)
            # TODO: https://git.sinntern.de/landmatrix/landmatrix/-/issues/404
            & (Q(from_user=user) | Q(to_user=user))
        ).update(processed_by_receiver=True)

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
) -> list[int]:
    role = get_user_role(user)
    if not role:
        raise GraphQLError("not authorized")

    # verify that the form is correct
    ObjectForm = DealForm if otype == "deal" else InvestorForm
    form = ObjectForm(payload)
    if not form.is_valid():
        raise ValidationError(dict(form.errors.items()))

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

    # retrieve the live object; update it with the payload - don't save.
    obj = Object.objects.get(id=obj_id)
    obj.update_from_dict(payload)
    obj.recalculate_fields()
    obj.modified_at = timezone.now()

    # this is a live Object for which we create a new Version,
    # or it is the version of the currently active Deal
    if not obj_version_id or (
        ObjectVersion.objects.filter(object_id=obj_id).first().id == obj_version_id
        and obj.draft_status is None
        and obj.status == 3
    ):
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

        # we create a new version if the Draft is already Review or Activation,
        # or the author is not the current user
        if (
            obj.draft_status in [DRAFT_STATUS["REVIEW"], DRAFT_STATUS["ACTIVATION"]]
        ) or obj_version.created_by_id != user.id:

            oldstatus = obj.draft_status

            obj_version.id = None
            obj_version.created_by = user
            obj_version.created_at = timezone.now()
            obj_version.modified_by = user

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
            Object.objects.filter(id=obj.id).update(
                current_draft=obj_version, draft_status=DRAFT_STATUS["DRAFT"]
            )
        else:
            if obj_version.serialized_data["draft_status"] == DRAFT_STATUS["REJECTED"]:
                add_workflow_info(
                    otype=otype,
                    obj=obj,
                    obj_version=obj_version,
                    from_user=user,
                    draft_status_before=DRAFT_STATUS["REJECTED"],
                    draft_status_after=DRAFT_STATUS["DRAFT"],
                )
                obj_version.serialized_data["draft_status"] = DRAFT_STATUS["DRAFT"]
                Object.objects.filter(id=obj.id).update(
                    current_draft=obj_version, draft_status=DRAFT_STATUS["DRAFT"]
                )

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

        if (
            obj.versions.count()
            and not obj.versions.all()[0].serialized_data["draft_status"]
        ):
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


# noinspection PyShadowingBuiltins
def resolve_toggle_workflow_info_unread(_obj, _info, id: int, type: str) -> bool:
    if type == "DealWorkflowInfo":
        wi = DealWorkflowInfo.objects.get(id=id)
        wi.processed_by_receiver = not wi.processed_by_receiver
        wi.save()
        return True
    elif type == "InvestorWorkflowInfo":
        wi = InvestorWorkflowInfo.objects.get(id=id)
        wi.processed_by_receiver = not wi.processed_by_receiver
        wi.save()
        return True
    return False


def resolve_object_copy(_obj, info, otype: OType, obj_id: int) -> dict:
    user = info.context["request"].user
    Object = Deal if otype == "deal" else Investor
    ObjectVersion = DealVersion if otype == "deal" else InvestorVersion

    obj = Object.objects.get(id=obj_id)
    obj.id = None

    old_comp_id = None
    if otype == "deal":
        old_comp_id = obj.operating_company_id
        obj.operating_company = None

    obj.current_draft = None
    obj.recalculate_fields()
    obj.created_by = user
    obj.created_at = timezone.now()
    obj.modified_by = user
    obj.modified_at = timezone.now()
    obj.status = obj.draft_status = DRAFT_STATUS["DRAFT"]

    obj.save()
    if otype == "deal":
        obj.operating_company_id = old_comp_id
        obj.save()

    obj_version = ObjectVersion.from_object(obj, created_by=user)
    Object.objects.filter(id=obj.id).update(current_draft=obj_version)
    add_workflow_info(
        otype=otype,
        obj=obj,
        obj_version=obj_version,
        from_user=user,
        draft_status_after=obj.draft_status,
        comment=f"Copied from {otype} #{obj_id}",
    )

    return {"objId": obj.id, "objVersion": obj_version.id}
