from typing import Literal, Type, cast

from ariadne.graphql import GraphQLError

from django.core.exceptions import ValidationError
from django.db.models import Model, Q
from django.utils import timezone

from apps.accounts.models import User, UserRole
from apps.landmatrix.forms.deal import DealForm
from apps.landmatrix.forms.investor import InvestorForm
from apps.landmatrix.models.abstracts import DRAFT_STATUS, STATUS, WorkflowInfo
from apps.landmatrix.models.deal import Deal, DealVersion, DealWorkflowInfo
from apps.landmatrix.models.investor import (
    Investor,
    InvestorVersion,
    InvestorWorkflowInfo,
)
from apps.utils import ecma262

from .user_utils import send_comment_to_user

OType = Literal["deal", "investor"]


DraftStatus = Literal["DRAFT", "REVIEW", "ACTIVATION", "REJECTED", "TO_DELETE"]


# @overload
# def add_workflow_info(
#     otype: Literal["deal"],
#     obj: Deal,
#     obj_version: DealVersion | None = None,
#     **kwargs,
# ) -> DealWorkflowInfo:
#     ...
#
#
# @overload
# def add_workflow_info(
#     otype: Literal["investor"],
#     obj: Investor,
#     obj_version: InvestorVersion | None = None,
#     **kwargs,
# ) -> InvestorWorkflowInfo:
#     ...


def add_workflow_info(
    otype: OType,
    obj: Deal | Investor,
    obj_version: DealVersion | InvestorVersion | None = None,
    **kwargs,
) -> DealWorkflowInfo | InvestorWorkflowInfo:
    if otype == "deal":
        return DealWorkflowInfo.objects.create(
            deal=cast(Deal, obj),
            deal_version=cast(DealVersion | None, obj_version),
            **kwargs,
        )
    else:
        return InvestorWorkflowInfo.objects.create(
            investor=cast(Investor, obj),
            investor_version=cast(InvestorVersion | None, obj_version),
            **kwargs,
        )


def add_object_comment(
    otype: OType,
    user: User,
    obj_id: int,
    obj_version_id: int,
    comment: str,
    to_user_id: int | None = None,
) -> None:
    if not (user.is_authenticated and user.role):
        raise GraphQLError("MISSING_AUTHORIZATION")

    Object: Type[Deal | Investor] = Deal if otype == "deal" else Investor
    obj: Deal | Investor = Object.objects.get(id=obj_id)

    obj_version: DealVersion | InvestorVersion | None = None
    draft_status: DraftStatus | None = None

    if obj_version_id:
        ObjectVersion: Type[DealVersion | InvestorVersion] = (
            DealVersion if otype == "deal" else InvestorVersion
        )
        obj_version = ObjectVersion.objects.get(id=obj_version_id)
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
    comment: str | None = None,
    to_user_id: int | None = None,
    fully_updated: bool = False,  # only relevant on "TO_REVIEW"
) -> list[int]:
    if not (user.is_authenticated and user.role):
        raise GraphQLError("MISSING_AUTHORIZATION")
    Object: Type[Deal | Investor] = Deal if otype == "deal" else Investor
    ObjectVersion: Type[DealVersion | InvestorVersion] = (
        DealVersion if otype == "deal" else InvestorVersion
    )
    obj: Deal | Investor = Object.objects.get(id=obj_id)
    obj_version: DealVersion | InvestorVersion = ObjectVersion.objects.get(
        id=obj_version_id
    )

    old_draft_status = obj_version.serialized_data["draft_status"]

    if obj.versions.first() != obj_version:
        raise GraphQLError("EDITING_OLD_VERSION")

    if transition == "TO_REVIEW":
        if not (obj_version.created_by == user or user.role >= UserRole.EDITOR):
            raise GraphQLError("MISSING_AUTHORIZATION")

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
        old_wfi: WorkflowInfo | None = obj.workflowinfos.last()
        if (
            old_wfi
            and old_wfi.draft_status_before in [2, 3]
            and old_wfi.draft_status_after == 1
            and old_wfi.to_user == user
        ):
            old_wfi.resolved = True
            old_wfi.save()
            send_comment_to_user(obj, "", user, old_wfi.from_user.id, obj_version_id)

    elif transition == "TO_ACTIVATION":
        if user.role < UserRole.EDITOR:
            raise GraphQLError("MISSING_AUTHORIZATION")
        draft_status = DRAFT_STATUS["ACTIVATION"]
        obj_version.serialized_data["draft_status"] = draft_status
        obj_version.save()
        Object.objects.filter(id=obj_id).update(draft_status=draft_status)
    elif transition == "ACTIVATE":
        if user.role < UserRole.ADMINISTRATOR:
            raise GraphQLError("MISSING_AUTHORIZATION")
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
        # close unresolved workflowinfos
        obj.workflowinfos.all().update(resolved=True)
    elif transition == "TO_DRAFT":
        if user.role < UserRole.EDITOR:
            raise GraphQLError("MISSING_AUTHORIZATION")
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
        ).update(resolved=True)

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
    obj_version_id: int | None = None,
    payload: dict | None = None,
) -> list[int]:
    if not (user.is_authenticated and user.role):
        raise GraphQLError("MISSING_AUTHORIZATION")

    if payload is None:
        payload = {}

    # verify that the form is correct
    ObjectForm = DealForm if otype == "deal" else InvestorForm
    form = ObjectForm(payload)
    if not form.is_valid():
        raise ValidationError(dict(form.errors.items()))

    Object: Type[Deal | Investor] = Deal if otype == "deal" else Investor
    ObjectVersion: Type[DealVersion | InvestorVersion] = (
        DealVersion if otype == "deal" else InvestorVersion
    )

    # this is a new Object
    if obj_id == -1:
        if "country" not in payload.keys():
            raise GraphQLError("COUNTRY_IS_MANDATORY")

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
        if not (obj_version.created_by == user or user.role >= UserRole.EDITOR):
            raise GraphQLError("MISSING_AUTHORIZATION")

        if obj.versions.first() != obj_version:
            raise GraphQLError("EDITING_OLD_VERSION")

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
    obj_version_id: int | None = None,
    comment: str | None = None,
) -> bool:
    if not (user.is_authenticated and user.role):
        raise GraphQLError("MISSING_AUTHORIZATION")

    Object: Type[Deal | Investor] = Deal if otype == "deal" else Investor
    obj: Deal | Investor = Object.objects.get(id=obj_id)

    # if it's just a draft,
    if obj_version_id:
        ObjectVersion: Type[DealVersion | InvestorVersion] = (
            DealVersion if otype == "deal" else InvestorVersion
        )
        obj_version: DealVersion | InvestorVersion = ObjectVersion.objects.get(
            id=obj_version_id
        )
        if not (obj_version.created_by == user or user.role >= UserRole.EDITOR):
            raise GraphQLError("MISSING_AUTHORIZATION")
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
        if user.role < UserRole.ADMINISTRATOR:
            raise GraphQLError("MISSING_AUTHORIZATION")
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
def resolve_resolve_workflow_info(_obj, info, id: int, type: str) -> bool:
    user = info.context["request"].user
    if not (user.is_authenticated and user.role):
        raise GraphQLError("MISSING_AUTHORIZATION")

    wi: DealWorkflowInfo | InvestorWorkflowInfo
    if type == "DealWorkflowInfo":
        wi = DealWorkflowInfo.objects.get(id=id)
    elif type == "InvestorWorkflowInfo":
        wi = InvestorWorkflowInfo.objects.get(id=id)
    else:
        return False
    wi.resolved = True
    wi.save()
    return True


# noinspection PyShadowingBuiltins
def resolve_add_workflow_info_reply(
    _obj,
    info,
    id: int,
    type: str,
    from_user_id: int,
    comment: str,
) -> bool:
    user = info.context["request"].user
    if not (user.is_authenticated and user.role):
        raise GraphQLError("MISSING_AUTHORIZATION")

    wi: DealWorkflowInfo | InvestorWorkflowInfo
    if type == "DealWorkflowInfo":
        wi = DealWorkflowInfo.objects.get(id=id)
    elif type == "InvestorWorkflowInfo":
        wi = InvestorWorkflowInfo.objects.get(id=id)
    else:
        return False
    if not wi.replies:
        wi.replies = []
    wi.replies += [
        {
            "timestamp": timezone.now().isoformat(),
            "user_id": from_user_id,
            "comment": comment,
        }
    ]
    wi.save()
    return True


def resolve_object_copy(_obj, info, otype: OType, obj_id: int) -> dict:
    user = info.context["request"].user
    if not (user.is_authenticated and user.role):
        raise GraphQLError("MISSING_AUTHORIZATION")

    Object: Type[Deal | Investor] = Deal if otype == "deal" else Investor
    ObjectVersion: Type[DealVersion | InvestorVersion] = (
        DealVersion if otype == "deal" else InvestorVersion
    )
    obj: Deal | Investor = Object.objects.get(id=obj_id)
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


def get_foreign_keys(model: Type[Model]) -> dict[str, Type[Model]]:
    return {
        x.name: x.related_model  # type: ignore
        for x in model._meta.fields
        if x.__class__.__name__ == "ForeignKey"
    }
