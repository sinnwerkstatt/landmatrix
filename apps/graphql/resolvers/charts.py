from collections import defaultdict
from typing import Any

from django.db.models import Q
from graphql import GraphQLResolveInfo

from apps.graphql.tools import parse_filters
from apps.landmatrix.models import Country
from apps.landmatrix.models.deal import DealTopInvestors, Deal

# def resolve_aggregations(obj: Any, info: GraphQLResolveInfo):
#     neg = Deal.objects.values("current_negotiation_status").annotate(Sum("deal_size"))


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


def resolve_web_of_transnational_deals(
    obj: Any, info: GraphQLResolveInfo, filters=None
):
    deals = Deal.objects.active()
    if filters:
        print(filters)
        filtered_filters = [
            f
            for f in filters
            if f["field"] not in ["country_id", "country.fk_region_id"]
        ]
        print(filtered_filters)

        deals = deals.filter(parse_filters(filtered_filters))

    deals_investors = (
        DealTopInvestors.objects.filter(investor__status__in=(2, 3))
        .filter(deal_id__in=deals.values_list("id", flat=True))
        .prefetch_related("deal")
        .prefetch_related("investor")
        .order_by("deal__country_id")
    )

    _relevant_countries = set()
    retdings = defaultdict(dict)
    for deal_invest in deals_investors:
        dc_id = deal_invest.deal.country_id
        ic_id = deal_invest.investor.country_id
        _relevant_countries.update({dc_id, ic_id})
        if dc_id and ic_id:
            if retdings.get(dc_id) and retdings[dc_id].get(ic_id):
                retdings[dc_id][ic_id]["size"] += deal_invest.deal.deal_size
                retdings[dc_id][ic_id]["count"] += 1
            else:
                retdings[dc_id][ic_id] = {
                    "size": deal_invest.deal.deal_size,
                    "count": 1,
                }

    country_dict = {c.id: c for c in Country.objects.filter(id__in=_relevant_countries)}

    regions = defaultdict(list)
    for country_id, country in country_dict.items():
        imports = []
        # regiondata = defaultdict(dict)
        for k, v in retdings[country_id].items():
            imp_c = country_dict[k]
            short_name = LONG_COUNTRIES.get(imp_c.name, imp_c.name)
            imports += [f"lama.{imp_c.fk_region_id}.{short_name}"]
            # regiondata_for_x = regiondata.get(imp_c.fk_region_id)
            # if regiondata_for_x:
            #     regiondata_for_x["size"] += v["size"]
            #     regiondata_for_x["count"] += v["count"]
            # else:
            #     regiondata[imp_c.fk_region_id] = {
            #         "size": v["size"],
            #         "count": v["count"],
            #     }

        short_name = LONG_COUNTRIES.get(country.name, country.name)
        regions[country.fk_region_id] += [
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


def country_investments(obj: Any, info: GraphQLResolveInfo, id):
    deals_investors = (
        DealTopInvestors.objects.filter(
            Q(deal__country_id=id) | Q(investor__country_id=id)
        )
        .filter(
            deal__status__in=(2, 3),
            investor__status__in=(2, 3),
            # deal__is_public=True,
        )
        .prefetch_related("deal")
        .prefetch_related("investor")
    )
    invested_regions = defaultdict(dict)
    investing_regions = defaultdict(dict)
    for invest in deals_investors:
        # TODO: do we count these?
        # if invest.deal.country_id == invest.investor.country_id:
        #     continue
        if invest.investor.country_id == id:
            reg_id = invest.deal.country.fk_region_id
            if invested_regions.get(reg_id):
                invested_regions[reg_id]["count"] += 1
                invested_regions[reg_id]["size"] += invest.deal.deal_size
            else:
                invested_regions[reg_id] = {"count": 1, "size": invest.deal.deal_size}
        else:
            reg_id = invest.investor.country.fk_region_id

            if investing_regions.get(reg_id):
                investing_regions[reg_id]["count"] += 1
                investing_regions[reg_id]["size"] += invest.deal.deal_size
            else:
                investing_regions[reg_id] = {"count": 1, "size": invest.deal.deal_size}
    return {"invested": invested_regions, "investing": investing_regions}
