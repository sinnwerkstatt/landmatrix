from django.template.defaultfilters import slugify
from django.db.models import Sum, Count

from api.query_sets.fake_query_set_with_subquery import FakeQuerySetWithSubquery
from api.query_sets.transnational_deals_query_set import TransnationalDealsQuerySet
from landmatrix.models import Country
from api.elasticsearch import es_search


class Top10InvestorCountriesQuerySet(FakeQuerySetWithSubquery):
    def all(self):
        # FIXME: Filter by active activities
        countries = Country.objects.annotate(hectares=Sum("investor__investoractivitysize__deal_size"),
                                             deals=Count("investor__investoractivitysize__fk_activity"))
        countries = countries.values('id', 'slug', 'name', 'hectares', 'deals')
        countries = countries.filter(hectares__isnull=False)
        countries = countries.order_by('-hectares')
        return countries


class Top10TargetCountriesQuerySet(FakeQuerySetWithSubquery):
    def all(self):
        # FIXME: Filter by active activities
        query = {
                "match_all": {}
        }
        aggregations = {
            "by_target_country": {
                "terms": {
                    "field": "target_country",
                    "size": 10000
                },
                "aggregations": {
                    "hectares": {
                        "sum": {
                            "field": "deal_size_export"
                        }
                    },
                    "deals": {
                        "cardinality": {
                            "field": "activity_identifier"
                        }
                    }
                }
            }
        }
        aggs = es_search.aggregate(aggregations, query=query)['by_target_country']
        names = dict(((c['id'], c) for c in Country.objects.values('id', 'slug', 'name')))
        countries = []
        for agg in aggs:
            if not agg['key']:
                continue
            country = names[int(agg['key'])]
            country['hectares'] = agg['hectares']['value'] or 0
            country['deals'] = agg['deals']['value'] or 0
            countries.append(country)
        return countries


class Top10CountriesQuerySet:

    def __init__(self, get_data):
        self.get_data = get_data

    def all(self):
        output = {
            "investor_country": [],
            "target_country": [],
        }
        for c in get_top_10_investor_countries(self.get_data):
            country = TransnationalDealsQuerySet.LONG_COUNTRIES.get(c['name'], c['name'])
            output["investor_country"].append(
                {"name": country, "slug": c['slug'], "hectares": c['hectares'], "id": c['id'], "deals": c['deals']}
            )
        for c in get_top_10_target_countries(self.get_data):
            country = TransnationalDealsQuerySet.LONG_COUNTRIES.get(c['name'], c['name'])
            output["target_country"].append(
                {"name": country, "slug": c['slug'], "hectares": c['hectares'], "id":c['id'], "deals": c['deals']}
            )
        return output


def get_top_10_investor_countries(get):
    queryset = Top10InvestorCountriesQuerySet(get)
    return queryset.all()


def get_top_10_target_countries(get):
    queryset = Top10TargetCountriesQuerySet(get)
    return queryset.all()
