from typing import Any

from django.utils import timezone
from graphql import GraphQLResolveInfo, GraphQLError

from apps.graphql.tools import get_fields, parse_filters
from apps.landmatrix.models import Investor, Deal
from apps.landmatrix.models.gndinvestor import InvestorVersion
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
    add_involvements = False
    filtered_fields = []
    for field in fields:
        if "versions" in field:
            add_versions = True
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


def resolve_investor_edit(_, info, id, version=None, payload: dict = None) -> dict:
    user = info.context["request"].user
    if not user.is_authenticated:
        raise GraphQLError("not authorized")

    # this is a new Investor
    if id == -1:
        investor = Investor()
        investor.update_from_dict(payload)
        investor.status = investor.draft_status = Investor.DRAFT_STATUS_DRAFT
        investor.save()
        rev = Revision.objects.create(
            date_created=timezone.now(), user=user, comment=""
        )
        Version.create_from_obj(investor, revision_id=rev.id)
        return {"investorId": investor.id, "investorVersion": rev.id}

    # TODO make sure user is allowed to edit this Investor.

    # investor = Investor.objects.get(id=id)
    # investor.update_from_dict(payload)
    # investor.recalculate_fields()
    #
    # # this is a live Deal for which we create a new Version
    # if not version:
    #     investor.draft_status = Investor.DRAFT_STATUS_DRAFT
    #     rev = investor.save_revision(date_created=timezone.now(), user=user)
    #     investor.objects.filter(id=id).update(draft_status=Investor.DRAFT_STATUS_DRAFT)
    # # we update the existing version.
    # else:
    #     rev = Revision.objects.get(id=version)
    #     investor_version = InvestorVersion.objects.get(revision=rev)
    #     investor_version.update_from_obj(investor)
    #     investor_version.save()
    #
    # return {"investorId": id, "investorVersion": rev.id}
