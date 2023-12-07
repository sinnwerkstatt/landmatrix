from django.db import connection
from django.db.models import Count, F, Sum

from apps.graphql.tools import parse_filters
from apps.landmatrix.charts import get_deal_top_investments, web_of_transnational_deals
from apps.landmatrix.models.deal import Deal


def resolve_global_map_of_investments(_obj, _info, filters=None):
    deals = Deal.objects.active()
    if filters:
        deals = deals.filter(parse_filters(filters))
    return get_deal_top_investments(deals)


def resolve_web_of_transnational_deals(_obj, _info, filters=None):
    deals = Deal.objects.active()
    if filters:
        deals = deals.filter(parse_filters(filters))
    return web_of_transnational_deals(deals)


# noinspection PyShadowingBuiltins
def country_investments_and_rankings(_obj, _info, id, filters=None):
    investments = get_deal_top_investments(filters)

    return {
        "investing": [
            {"country_id": country_id, "size": bucket["size"], "count": bucket["count"]}
            for country_id, bucket in investments["incoming"][id].items()
        ],
        "invested": [
            {"country_id": country_id, "size": bucket["size"], "count": bucket["count"]}
            for country_id, bucket in investments["outgoing"][id].items()
        ],
    }


def global_rankings(_obj, _info, count=10, filters=None):
    qs = Deal.objects.active()

    if filters:
        qs = qs.filter(parse_filters(filters))

    return {
        "ranking_deal": list(qs.get_deal_country_rankings())[:count],
        "ranking_investor": list(qs.get_investor_country_rankings())[:count],
    }


def create_statistics(country_id=None, region_id=None):
    select_clause = "SELECT count(distinct(d.id))"
    from_clause = "FROM landmatrix_deal AS d"
    where_clause = "WHERE d.status IN (2,3) AND d.is_public=True"

    if country_id:
        where_clause += f" AND d.country_id={country_id}"
    if region_id:
        from_clause += " INNER JOIN landmatrix_country AS c ON (d.country_id = c.id)"
        where_clause += f" AND c.region_id={region_id}"

    cursor = connection.cursor()

    cursor.execute(f"{select_clause} {from_clause} {where_clause}")
    deals_public_count = cursor.fetchone()[0]

    cursor.execute(
        f"""
            {select_clause}
            {from_clause}
            {where_clause}
            AND jsonb_array_length(d.datasources) > 1
        """
    )
    deals_public_multi_ds_count = cursor.fetchone()[0]

    cursor.execute(
        f"""
            {select_clause}
            {from_clause}, jsonb_array_elements(d.locations) AS l
            {where_clause}
            AND (
              l->>'level_of_accuracy' in ('EXACT_LOCATION','COORDINATES')
              OR l->>'areas' IS NOT NULL
            )
        """
    )
    deals_public_high_geo_accuracy = cursor.fetchone()[0]

    cursor.execute(
        f"""
            {select_clause}
            {from_clause}, jsonb_array_elements(d.locations) AS l
            {where_clause}
            AND l->>'areas' IS NOT NULL
        """
    )
    deals_public_polygons = cursor.fetchone()[0]

    return {
        "deals_public_count": deals_public_count,
        "deals_public_multi_ds_count": deals_public_multi_ds_count,
        "deals_public_high_geo_accuracy": deals_public_high_geo_accuracy,
        "deals_public_polygons": deals_public_polygons,
    }


def resolve_statistics(_obj, _info, country_id=None, region_id=None):
    return create_statistics(country_id, region_id)


def resolve_deal_aggregations(_obj, info, fields, subset="PUBLIC", filters=None):
    deals = Deal.objects.visible(user=info.context["request"].user, subset=subset)
    if filters:
        deals = deals.filter(parse_filters(filters))

    aggs = {}
    for field in fields:
        aggs[field] = list(
            deals.order_by(field, "id")
            .values(value=F(field))
            .annotate(count=Count("pk"))
            .annotate(size=Sum("deal_size"))
        )

    return aggs
