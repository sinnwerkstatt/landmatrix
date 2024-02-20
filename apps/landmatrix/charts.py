from collections import defaultdict

from apps.landmatrix.models.country import Country
from apps.landmatrix.models.new import (
    DealHull,
    DealTopInvestors2,
    InvestorHull,
    DealVersion2,
)
from apps.landmatrix.utils import parse_filters

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


def get_deal_top_investments(request):
    dh = DealHull.objects.active().filter(parse_filters(request))
    deals = DealVersion2.objects.filter(id__in=dh.values_list("active_version_id"))

    investors = InvestorHull.objects.exclude(active_version_id=None).filter(
        deleted=False
    )

    incoming = investmentsdict()
    outgoing = investmentsdict()

    for deal_country_id, investor_country_id, size in (
        DealTopInvestors2.objects.filter(
            investorhull__in=investors, dealversion2__in=deals
        )
        .values_list(
            "dealversion2__deal__country_id",
            "investorhull__active_version__country_id",
            "dealversion2__deal_size",
        )
        .order_by("dealversion2__deal__country_id")
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


def web_of_transnational_deals(request):
    investments = get_deal_top_investments(request)
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
