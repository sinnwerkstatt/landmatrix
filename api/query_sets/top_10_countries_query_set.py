from api.query_sets.fake_query_set_with_subquery import FakeQuerySetWithSubquery
from api.query_sets.transnational_deals_query_set import TransnationalDealsQuerySet
from django.template.defaultfilters import slugify



class Top10InvestorCountriesQuerySet(FakeQuerySetWithSubquery):

    FIELDS = [
        ('investor_country', 'investor_country'),
        ('investor_country_id', 'investor_country_id'),
        ('hectares',          "COALESCE(ROUND(SUM(a.deal_size)), 0)"),
        ('deals',         'COUNT(DISTINCT a.activity_identifier)'),
    ]
    SUBQUERY_FIELDS = [
        ('investor_country', 'investor_country.name'),
        ('investor_country_id', 'investor_country.id'),
    ]
    ADDITIONAL_JOINS = [
        "LEFT JOIN landmatrix_investoractivityinvolvement AS iai            ON iai.fk_activity_id = a.id",
        "LEFT JOIN landmatrix_investor                  AS operational_stakeholder ON iai.fk_investor_id = operational_stakeholder.id",
        "LEFT JOIN landmatrix_investorventureinvolvement AS ivi             ON ivi.fk_venture_id = operational_stakeholder.id",
        "LEFT JOIN landmatrix_investor                  AS stakeholder      ON ivi.fk_investor_id = stakeholder.id",
        "LEFT JOIN landmatrix_country                   AS investor_country ON stakeholder.fk_country_id = investor_country.id",
    ]
    ADDITIONAL_WHERES = ["investor_country.id IS NOT NULL"]
    GROUP_BY = ['sub.investor_country', 'sub.investor_country_id']
    ORDER_BY = ['hectares DESC']
    LIMIT = 100


class Top10TargetCountriesQuerySet(FakeQuerySetWithSubquery):

    FIELDS = [
        ('target_country', 'sub.target_country'),
        ('target_country_id', 'sub.target_country_id'),
        ('hectares',          "COALESCE(ROUND(SUM(a.deal_size)), 0)"),
        ('deals',         'COUNT(DISTINCT a.activity_identifier)'),
    ]
    SUBQUERY_FIELDS = [
        ('target_country', 'deal_country.name'),
        ('target_country_id', 'deal_country.id'),
    ]
    ADDITIONAL_JOINS = [
        "LEFT JOIN landmatrix_investoractivityinvolvement AS iai            ON iai.fk_activity_id = a.id",
        "LEFT JOIN landmatrix_investor                  AS operational_stakeholder ON iai.fk_investor_id = operational_stakeholder.id",
        "LEFT JOIN landmatrix_investorventureinvolvement AS ivi             ON ivi.fk_venture_id = operational_stakeholder.id",
        "LEFT JOIN landmatrix_investor                  AS stakeholder      ON ivi.fk_investor_id = stakeholder.id",
        "LEFT JOIN landmatrix_activityattribute         AS target_country   ON a.id = target_country.fk_activity_id AND target_country.name = 'target_country'",
        "LEFT JOIN landmatrix_country                   AS deal_country     ON CAST(target_country.value AS NUMERIC) = deal_country.id",
    ]
    ADDITIONAL_WHERES = ["stakeholder.fk_country_id IS NOT NULL"]
    GROUP_BY = ['sub.target_country', 'sub.target_country_id']
    ORDER_BY = ['hectares DESC']
    LIMIT = 100


class Top10CountriesQuerySet:

    def __init__(self, get_data):
        self.get_data = get_data

    def all(self):
        output = {
            "investor_country": [],
            "target_country": [],
        }
        for c in get_top_10_investor_countries(self.get_data):
            country = TransnationalDealsQuerySet.LONG_COUNTRIES.get(c['investor_country'], c['investor_country'])
            output["investor_country"].append(
                {"name": country, "slug": slugify(c['investor_country']), "hectares": c['hectares'], "id": c['investor_country_id'], "deals": c['deals']}
            )
        for c in get_top_10_target_countries(self.get_data):
            country = TransnationalDealsQuerySet.LONG_COUNTRIES.get(c['target_country'], c['target_country'])
            output["target_country"].append(
                {"name": country, "slug": slugify(c['target_country']), "hectares": c['hectares'], "id":c['target_country_id'], "deals": c['deals']}
            )
        return output


def get_top_10_investor_countries(get):
    queryset = Top10InvestorCountriesQuerySet(get)
    return queryset.all()


def get_top_10_target_countries(get):
    queryset = Top10TargetCountriesQuerySet(get)
    return queryset.all()
