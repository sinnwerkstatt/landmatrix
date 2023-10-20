from collections import defaultdict

from django.db import connection
from django.db.models import Count, F, Sum

from apps.landmatrix.models.country import Country
from apps.landmatrix.models.deal import Deal, DealTopInvestors

from ..tools import parse_filters

LONG_COUNTRIES = {
    "United States of America": "USA*",
    "United Kingdom of Great Britain and Northern Ireland": "UK*",
    "China, Hong Kong Special Administrative Region": "China, Hong Kong*",
    "China, Macao Special Administrative Region": "China, Macao*",
    "Lao People's Democratic Republic": "Laos*",
    "United Republic of Tanzania": "Tanzania*",
    "Democratic Republic of the Congo": "DRC*",
    "Bolivia (Plurinational State of)": "Bolivia*",
    "The Former Yugoslav Republic of Macedonia": "Macedonia*",
    "Venezuela (Bolivarian Republic of)": "Venezuela*",
    "Republic of Moldova": "Moldova*",
    "United Arab Emirates": "Arab Emirates*",
    "Solomon Islands": "Solomon Iss*",
    "Russian Federation": "Russian Fed*",
    "Dominican Republic": "Dominican Rep*",
    "Papua New Guinea": "Papua New*",
    "Democratic People's Republic of Korea": "North Korea*",
    "Korea, Dem. People's Rep.": "North Korea*",
    "United States Virgin Islands": "Virgin Iss*",
    "Iran (Islamic Republic of)": "Iran*",
    "Syrian Arab Republic": "Syria*",
    "Republic of Korea": "South Korea*",
    "British Virgin Islands": "British Virgin Iss*",
}


def investmentsdict():
    """
    A dict representing incoming or outgoing investments between countries.

    Example:
        investments = investmentsdict()
        investments[from_country_id][to_country_id] = { 'size': 2000, 'count': 2 }
    """

    return defaultdict(
        lambda: defaultdict(
            lambda: dict(size=0, count=0),
        )
    )


def get_deal_top_investments(filters=None):
    deals = Deal.objects.active()
    if filters:
        deals = deals.filter(parse_filters(filters))

    incoming = investmentsdict()
    outgoing = investmentsdict()

    for deal_country_id, investor_country_id, size in (
        DealTopInvestors.objects.filter(investor__status__in=(2, 3), deal__in=deals)
        .values_list("deal__country_id", "investor__country_id", "deal__deal_size")
        .order_by("deal__country_id")
    ):
        # Ignore deals and investors without country association.
        if deal_country_id is None or investor_country_id is None:
            continue

        # Skip investments in own country.
        if deal_country_id == investor_country_id:
            continue

        incoming[deal_country_id][investor_country_id]["size"] += size
        incoming[deal_country_id][investor_country_id]["count"] += 1

        outgoing[investor_country_id][deal_country_id]["size"] += size
        outgoing[investor_country_id][deal_country_id]["count"] += 1

    return {
        "incoming": incoming,
        "outgoing": outgoing,
    }


def resolve_global_map_of_investments(_obj, _info, filters=None):
    investments = get_deal_top_investments(filters)
    return investments["incoming"]


def resolve_web_of_transnational_deals(_obj, _info, filters=None):
    investments = get_deal_top_investments(filters)
    countries = investments["incoming"].keys() | investments["outgoing"].keys()

    country_dict = {c.id: c for c in Country.objects.filter(id__in=countries)}

    regions = defaultdict(list)
    for country_id, country in country_dict.items():
        imports = []
        for k, v in investments["incoming"][country_id].items():
            imp_c = country_dict[k]
            short_name = LONG_COUNTRIES.get(imp_c.name, imp_c.name)
            imports += [f"lama.{imp_c.region_id}.{short_name}"]
        short_name = LONG_COUNTRIES.get(country.name, country.name)

        regions[country.region_id] += [
            {
                "id": country.id,
                "name": short_name,
                "imports": imports,
            }
        ]

    return {
        "name": "lama",
        "children": [{"name": x, "children": y} for (x, y) in regions.items()],
    }


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
