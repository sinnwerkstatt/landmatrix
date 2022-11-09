from collections import defaultdict

from django.db import connection
from django.db.models import Sum, Count, F

from apps.graphql.tools import parse_filters
from apps.landmatrix.models.country import Country
from apps.landmatrix.models.deal import DealTopInvestors, Deal

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


def _deal_investors(filters=None):
    deals = Deal.objects.active()
    if filters:
        deals = deals.filter(parse_filters(filters))

    deals_investors = (
        DealTopInvestors.objects.filter(investor__status__in=(2, 3))
        .filter(deal__in=deals)
        .prefetch_related("deal")
        .prefetch_related("investor")
        .order_by("deal__country_id")
    )

    relevant_countries = set()
    retdings = defaultdict(dict)
    for deal_invest in deals_investors:
        dc_id = deal_invest.deal.country_id
        ic_id = deal_invest.investor.country_id
        relevant_countries.update({dc_id, ic_id})
        if dc_id and ic_id:
            if retdings.get(dc_id) and retdings[dc_id].get(ic_id):
                retdings[dc_id][ic_id]["size"] += deal_invest.deal.deal_size
                retdings[dc_id][ic_id]["count"] += 1
            else:
                retdings[dc_id][ic_id] = {
                    "size": deal_invest.deal.deal_size,
                    "count": 1,
                }
    return {"links": retdings, "relevant_countries": relevant_countries}


def resolve_global_map_of_investments(_obj, _info, filters=None):
    deal_investors = _deal_investors(filters)
    return dict(deal_investors["links"])


def resolve_web_of_transnational_deals(_obj, _info, filters=None):
    deal_investors = _deal_investors(filters)
    _relevant_countries = deal_investors["relevant_countries"]

    country_dict = {c.id: c for c in Country.objects.filter(id__in=_relevant_countries)}

    regions = defaultdict(list)
    for country_id, country in country_dict.items():
        imports = []
        # regiondata = defaultdict(dict)
        for k, v in deal_investors["links"][country_id].items():
            imp_c = country_dict[k]
            short_name = LONG_COUNTRIES.get(imp_c.name, imp_c.name)
            imports += [f"lama.{imp_c.region_id}.{short_name}"]
            # regiondata_for_x = regiondata.get(imp_c.region_id)
            # if regiondata_for_x:
            #     regiondata_for_x["size"] += v["size"]
            #     regiondata_for_x["count"] += v["count"]
            # else:
            #     regiondata[imp_c.region_id] = {
            #         "size": v["size"],
            #         "count": v["count"],
            #     }

        short_name = LONG_COUNTRIES.get(country.name, country.name)
        regions[country.region_id] += [
            {
                "id": country.id,
                "name": short_name,
                "imports": imports,
                # "deals": regiondata,
            }
        ]

    return {
        "name": "lama",
        "children": [{"name": x, "children": y} for (x, y) in regions.items()],
    }


# noinspection PyShadowingBuiltins
def country_investments_and_rankings(_obj, _info, id, filters=None):
    deals = Deal.objects.active()
    if filters:
        deals = deals.filter(parse_filters(filters))
    active_dtis = DealTopInvestors.objects.filter(
        deal__in=deals,
        investor__status__in=(2, 3),
    )

    investing = list(
        active_dtis.filter(deal__country_id=id)
        .exclude(investor__country=None)
        .exclude(investor__country_id=id)
        .values(country_id=F("investor__country_id"))
        .order_by("country_id")
        .annotate(count=Count("deal"))
        .annotate(size=Sum("deal__deal_size"))
    )
    invested = list(
        active_dtis.filter(investor__country_id=id)
        .exclude(deal__country=None)
        .exclude(deal__country_id=id)
        .values(country_id=F("deal__country_id"))
        .order_by("country_id")
        .annotate(count=Count("deal"))
        .annotate(size=Sum("deal__deal_size"))
    )
    return {
        "investing": investing,
        "invested": invested,
        # deactivated for now
        # "ranking_deal": Deal.objects.active().get_deal_country_rankings(id),
        # "ranking_investor": Deal.objects.active().get_investor_country_rankings(id),
        "ranking_deal": None,
        "ranking_investor": None,
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
