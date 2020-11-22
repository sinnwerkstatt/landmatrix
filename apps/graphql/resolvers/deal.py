from typing import Any

from django.utils.html import linebreaks
from django_comments.models import Comment
from graphql import GraphQLResolveInfo

from apps.graphql.tools import get_fields, parse_filters
from apps.landmatrix.models import Deal, Country, Investor
from apps.landmatrix.models.deal import DealVersion
from apps.landmatrix.models.versions import Revision
from apps.utils import qs_values_to_dict


def map_raw_sql():
    sql = """
    select json_build_object(
    'id',ld.id,
    'deal_size',ld.deal_size,
    'country',(SELECT json_build_object('id',c.id,'name',c.name) from landmatrix_country c where c.id=ld.country_id),
    'locations',(
        SELECT json_agg(locs)
        from landmatrix_location locs where locs.deal_id=ld.id
        )
    ) from landmatrix_deal ld
    where ld.id=6869;
    """


def resolve_deal_version(deal_id, version, fields):
    rev = Revision.objects.get(id=version)

    deal = rev.dealversion_set.get().fields

    deal["locations"] = [v.fields for v in rev.locationversion_set.all()]
    deal["datasources"] = [v.fields for v in rev.datasourceversion_set.all()]
    deal["contracts"] = [v.fields for v in rev.contractversion_set.all()]

    if any(["versions" in field for field in fields]):
        deal["versions"] = [
            dv.to_dict() for dv in DealVersion.objects.filter(object_id=deal_id)
        ]

    if "operating_company" in deal:
        deal["operating_company"] = Investor.objects.get(id=deal["operating_company"])
    if "country" in deal:
        deal["country"] = Country.objects.get(id=deal["country"])
    return deal


def resolve_deal(obj, info: GraphQLResolveInfo, id, version=None):
    fields = get_fields(info, recursive=True, exclude=["__typename"])

    if version:
        return resolve_deal_version(id, version, fields)

    add_versions = False
    add_comments = False
    filtered_fields = []
    for field in fields:
        if "versions" in field:
            add_versions = True
        elif "comments" in field:
            add_comments = True
        else:
            filtered_fields += [field]

    visible_deals = Deal.objects.visible(info.context.user, "UNFILTERED").filter(id=id)
    if not visible_deals:
        return

    deal = qs_values_to_dict(
        visible_deals,
        filtered_fields,
        ["locations", "datasources", "contracts", "top_investors"],
    )[0]

    if add_versions:
        deal["versions"] = [
            dv.to_dict() for dv in DealVersion.objects.filter(object_id=id)
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
    qs = Deal.objects.visible(user=info.context.user, subset=subset).order_by(sort)

    if filters:
        qs = qs.filter(parse_filters(filters))

    fields = get_fields(info, recursive=True, exclude=["__typename"])

    if limit != 0:
        qs = qs[:limit]

    return qs_values_to_dict(
        qs, fields, ["locations", "datasources", "contracts", "top_investors"]
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

    # TODO Ralph bitte bitte
    # if filters:
    #     qs = qs.filter(parse_filters(filters))

    if country_id:
        qs = qs.filter(serialized_data__0__fields__country=country_id)

    if region_id:
        country_ids = Country.objects.filter(fk_region_id=region_id).values_list(
            "id", flat=True
        )
        qs = qs.filter(serialized_data__0__fields__country__in=country_ids)

    return [dv.to_dict() for dv in qs]
