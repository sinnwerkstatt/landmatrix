from typing import Any

from django.utils import timezone
from graphql import GraphQLResolveInfo, GraphQLError

from apps.graphql.resolvers.user_utils import get_user_role, send_comment_to_user
from apps.graphql.tools import get_fields, parse_filters
from apps.landmatrix.models import Investor, Deal
from apps.landmatrix.models.gndinvestor import InvestorVersion, InvestorWorkflowInfo
from apps.landmatrix.models.versions import Revision, Version
from apps.landmatrix.utils import InvolvementNetwork
from apps.utils import qs_values_to_dict


def resolve_investor(
    obj: Any,
    info: GraphQLResolveInfo,
    id,
    version=None,
    subset="PUBLIC",
    involvements_depth: int = 4,
    involvements_include_ventures: bool = True,
):
    fields = get_fields(info, recursive=True, exclude=["__typename"])

    add_versions = False
    add_deals = False
    add_workflowinfos = False
    add_involvements = False
    filtered_fields = []
    for field in fields:
        if "versions" in field:
            add_versions = True
        elif "workflowinfos" in field:
            add_workflowinfos = True
        elif "deals" in field:
            add_deals = True
        elif "involvements" in field:
            add_involvements = True
        else:
            filtered_fields += [field]

    if version:
        rev = Revision.objects.get(id=version)
        investor = rev.investorversion_set.get().fields
        # investor["involvements"] = [
        #     v.fields for v in rev.investorventureinvolvementversion_set.all()
        # ]
    else:
        visible_investors = Investor.objects.visible(
            info.context["request"].user, subset
        ).filter(id=id)
        if not visible_investors:
            return
        investor = qs_values_to_dict(
            visible_investors,
            filtered_fields,
            ["involvements", "investors", "ventures"],
        )[0]

    if add_versions:
        investor["versions"] = [
            dv.to_dict() for dv in InvestorVersion.objects.filter(object_id=id)
        ]
    if add_workflowinfos:
        investor["workflowinfos"] = [
            dwi.to_dict()
            for dwi in InvestorWorkflowInfo.objects.filter(investor_id=id).order_by(
                "-timestamp"
            )
        ]
    if add_deals:
        investor["deals"] = (
            Deal.objects.visible(info.context["request"].user, subset)
            .filter(operating_company_id=id)
            .order_by("id")
        )
    if add_involvements:
        investor["involvements"] = InvolvementNetwork(
            involvements_include_ventures, max_depth=involvements_depth
        ).get_network(id)

    if not investor.get("investors"):
        investor["investors"] = []
    return investor


def resolve_investors(
    obj: Any,
    info: GraphQLResolveInfo,
    sort="id",
    limit=20,
    subset="PUBLIC",
    filters=None,
):
    qs = Investor.objects.visible(
        user=info.context["request"].user, subset=subset
    ).order_by(sort)

    fields = get_fields(info, recursive=True, exclude=["__typename"])

    if any(["involvements" in field for field in fields]):
        raise GraphQLError(
            "Querying involvements via multiple operating companies is too"
            " resource intensive. Please use single investor queries for this."
        )

    if filters:
        qs = qs.filter(parse_filters(filters))

    if limit != 0:
        qs = qs[:limit]

    return qs_values_to_dict(
        qs, fields, ["involvements", "ventures", "investors", "deals"]
    )


def resolve_investorversions(obj, info: GraphQLResolveInfo, filters=None):
    qs = InvestorVersion.objects.all()
    if filters:
        qs = qs.filter(parse_filters(filters))
    return [iv.to_dict() for iv in qs]


def resolve_add_investor_comment(
    _, info, id: int, version: int, comment: str, to_user_id=None
) -> dict:
    user = info.context["request"].user
    role = get_user_role(user)
    if not role:
        raise GraphQLError("not allowed")

    investor = Investor.objects.get(id=id)
    investor_version = None
    draft_status = None
    if version:
        investor_version = InvestorVersion.objects.get(revision_id=version)
        investor_v_obj = investor_version.retrieve_object()
        draft_status = investor_v_obj.draft_status

    InvestorWorkflowInfo.objects.create(
        investor=investor,
        investor_version=investor_version,
        from_user=user,
        to_user_id=to_user_id,
        draft_status_before=draft_status,
        draft_status_after=draft_status,
        comment=comment,
    )

    if to_user_id:
        send_comment_to_user(
            investor,
            comment,
            user,
            to_user_id,
            version,
        )

    return {"investorId": investor.id, "investorVersion": version}


def resolve_change_investor_status(
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
    if not role:
        raise GraphQLError("not allowed")

    investor = Investor.objects.get(id=id)
    rev = Revision.objects.get(id=version)
    investor_version = InvestorVersion.objects.get(revision=rev)

    investor_v_obj: Investor = investor_version.retrieve_object()
    old_draft_status = investor_v_obj.draft_status

    if transition == "TO_REVIEW":
        if not (
            investor_version.revision.user == user
            or role in ["ADMINISTRATOR", "EDITOR"]
        ):
            raise GraphQLError("not authorized")
        draft_status = Investor.DRAFT_STATUS_REVIEW
        investor_v_obj.draft_status = draft_status
        investor_version.update_from_obj(investor_v_obj).save()
        Investor.objects.filter(id=id).update(draft_status=draft_status)
    elif transition == "TO_ACTIVATION":
        if role not in ["ADMINISTRATOR", "EDITOR"]:
            raise GraphQLError("not authorized")
        draft_status = Investor.DRAFT_STATUS_ACTIVATION
        investor_v_obj.draft_status = draft_status
        investor_version.update_from_obj(investor_v_obj).save()
        Investor.objects.filter(id=id).update(draft_status=draft_status)
    elif transition == "ACTIVATE":
        if role != "ADMINISTRATOR":
            raise GraphQLError("not allowed")
        draft_status = None
        investor_v_obj.status = (
            Investor.STATUS_LIVE
            if investor.status == Investor.STATUS_DRAFT
            else Investor.STATUS_UPDATED
        )
        investor_v_obj.draft_status = draft_status
        investor_v_obj.save()
        investor_version.update_from_obj(investor_v_obj).save()
    elif transition == "TO_DRAFT":
        if role not in ["ADMINISTRATOR", "EDITOR"]:
            raise GraphQLError("not authorized")
        draft_status = investor.draft_status = Investor.DRAFT_STATUS_DRAFT
        rev = Revision.objects.create(date_created=timezone.now(), user_id=to_user_id)
        Version.create_from_obj(investor, revision_id=rev.id)
        Investor.objects.filter(id=id).update(draft_status=draft_status)
    else:
        raise GraphQLError(f"unknown transition {transition}")

    InvestorWorkflowInfo.objects.create(
        investor=investor,
        investor_version=investor_version,
        from_user=user,
        to_user_id=to_user_id,
        draft_status_before=old_draft_status,
        draft_status_after=draft_status,
        comment=comment,
    )

    if to_user_id:
        send_comment_to_user(
            investor,
            comment,
            user,
            to_user_id,
            version,
        )

    return {"investorId": investor.id, "investorVersion": rev.id}


def resolve_investor_delete(_, info, id, version=None, comment=None) -> bool:
    user = info.context["request"].user
    role = get_user_role(user)
    if not role:
        raise GraphQLError("not authorized")

    investor = Investor.objects.get(id=id)
    # if it's just a draft,
    if version:
        investor_version = InvestorVersion.objects.get(revision_id=version)
        if not (
            investor_version.revision.user == user
            or role in ["ADMINISTRATOR", "EDITOR"]
        ):
            raise GraphQLError("not authorized")
        investor_v_obj = investor_version.retrieve_object()
        old_draft_status = investor_v_obj.draft_status
        investor_version.delete()
        InvestorWorkflowInfo.objects.create(
            investor=investor,
            from_user=user,
            draft_status_before=old_draft_status,
            draft_status_after=investor.status == Investor.STATUS_DELETED,
            comment=comment,
        )

        if (
            investor.versions.count()
            and not investor.versions.order_by("-id")[0].serialized_data[0]["fields"][
                "draft_status"
            ]
        ):
            # reset the Live version to "not having a draft" if we delete it.
            Investor.objects.filter(id=id).update(draft_status=None)

        if investor.versions.count() == 0 and investor.status == Investor.STATUS_DRAFT:
            Revision.objects.filter(investorversion__object_id=investor.id).delete()
            investor.delete()

    else:
        if role != "ADMINISTRATOR":
            raise GraphQLError("not authorized")
        investor.status = (
            Investor.STATUS_UPDATED
            if investor.status == Investor.STATUS_DELETED
            else Investor.STATUS_DELETED
        )
        investor.modified_at = timezone.now()
        investor.save()
        InvestorWorkflowInfo.objects.create(
            investor=investor,
            from_user=user,
            draft_status_before=(
                None
                if investor.status == Investor.STATUS_DELETED
                else Investor.DRAFT_STATUS_TO_DELETE
            ),
            draft_status_after=(
                Investor.DRAFT_STATUS_TO_DELETE
                if investor.status == Investor.STATUS_DELETED
                else None
            ),
            comment=comment,
        )
    return True


def resolve_investor_edit(_, info, id, version=None, payload: dict = None) -> dict:
    user = info.context["request"].user
    role = get_user_role(user)
    if not role:
        raise GraphQLError("not authorized")

    # this is a new Investor
    if id == -1:
        investor = Investor()
        investor.update_from_dict(payload)
        investor.modified_at = timezone.now()
        investor.status = investor.draft_status = Investor.DRAFT_STATUS_DRAFT
        investor.save()
        rev = Revision.objects.create(date_created=timezone.now(), user=user)
        investor_version = Version.create_from_obj(investor, revision_id=rev.id)
        InvestorWorkflowInfo.objects.create(
            investor=investor,
            investor_version=investor_version,
            from_user=user,
            draft_status_after=investor.draft_status,
        )
        return {"investorId": investor.id, "investorVersion": rev.id}

    investor = Investor.objects.get(id=id)
    investor.update_from_dict(payload)
    investor.modified_at = timezone.now()

    # this is a live Investor for which we create a new Version
    if not version:
        investor.draft_status = Investor.DRAFT_STATUS_DRAFT
        rev = Revision.objects.create(date_created=timezone.now(), user=user)
        Version.create_from_obj(investor, revision_id=rev.id)
        Investor.objects.filter(id=id).update(draft_status=Investor.DRAFT_STATUS_DRAFT)

        investor_version = InvestorVersion.objects.get(revision=rev)
        investor_v_obj = investor_version.retrieve_object()
        InvestorWorkflowInfo.objects.create(
            investor=investor,
            investor_version=investor_version,
            from_user=user,
            draft_status_before=None,
            draft_status_after=investor_v_obj.draft_status,
        )

    # we update the existing version.
    else:
        rev = Revision.objects.get(id=version)
        investor_version = InvestorVersion.objects.get(revision=rev)
        if not (
            investor_version.revision.user == user
            or role in ["ADMINISTRATOR", "EDITOR"]
        ):
            raise GraphQLError("not authorized")

        investor_version.update_from_obj(investor)
        if investor.draft_status in [
            Investor.DRAFT_STATUS_REVIEW,
            Investor.DRAFT_STATUS_ACTIVATION,
        ]:
            oldstatus = investor.draft_status
            rev = Revision.objects.create(date_created=timezone.now(), user=user)
            tmp_investor = investor_version.retrieve_object()
            tmp_investor.draft_status = Investor.DRAFT_STATUS_DRAFT
            dv = Version.create_from_obj(tmp_investor, revision_id=rev.id)
            InvestorWorkflowInfo.objects.create(
                investor=investor,
                investor_version=dv,
                from_user=user,
                draft_status_before=oldstatus,
                draft_status_after=Investor.DRAFT_STATUS_DRAFT,
            )
        else:
            investor_version.save()
            if investor.status == Investor.STATUS_DRAFT:
                investor.save()

    return {"investorId": id, "investorVersion": rev.id}
