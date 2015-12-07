from api.query_sets.fake_query_set_with_subquery import FakeQuerySetWithSubquery
from api.query_sets.transnational_deals_query_set import TransnationalDealsQuerySet
from django.template.defaultfilters import slugify

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class Top10InvestorCountriesQuerySet(FakeQuerySetWithSubquery):

    FIELDS = [
        ('investor_country', 'investor_country'),
        ('investor_country_id', 'investor_country_id'),
        ('hectares',          "COALESCE(ROUND(SUM(pi.deal_size)), 0)"),
        ('deals',         'COUNT(DISTINCT a.activity_identifier)'),
    ]
    SUBQUERY_FIELDS = [
        ('investor_country', 'investor_country.name'),
        ('investor_country_id', 'investor_country.id'),
    ]
    ADDITIONAL_JOINS = [
        "LEFT JOIN landmatrix_stakeholder               AS s                ON i.fk_stakeholder_id = s.id",
        "LEFT JOIN landmatrix_stakeholderattributegroup AS skvf1            ON s.id = skvf1.fk_stakeholder_id AND skvf1.attributes ? 'country'",
        "LEFT JOIN landmatrix_country                   AS investor_country ON CAST(skvf1.attributes->'country' AS NUMERIC) = investor_country.id",
        # "LEFT JOIN landmatrix_activityattributegroup    AS negotiation      ON a.id = negotiation.fk_activity_id AND negotiation.attributes ? 'pi_negotiation_status'",
        # "LEFT JOIN landmatrix_activityattributegroup    AS deal_scope       ON a.id = deal_scope.fk_activity_id AND deal_scope.attributes ? 'deal_scope'"
    ]
    ADDITIONAL_WHERES = ["investor_country.id IS NOT NULL"]
    GROUP_BY = ['sub.investor_country', 'sub.investor_country_id']
    ORDER_BY = ['hectares DESC']
    LIMIT = 10


class Top10TargetCountriesQuerySet(FakeQuerySetWithSubquery):

    FIELDS = [
        ('target_country', 'sub.target_country'),
        ('target_country_id', 'sub.target_country_id'),
        ('hectares',          "COALESCE(ROUND(SUM(pi.deal_size)), 0)"),
        ('deals',         'COUNT(DISTINCT a.activity_identifier)'),
    ]
    SUBQUERY_FIELDS = [
        ('target_country', 'deal_country.name'),
        ('target_country_id', 'deal_country.id'),
    ]
    ADDITIONAL_JOINS = [
        "LEFT JOIN landmatrix_stakeholder               AS s                ON i.fk_stakeholder_id = s.id",
        "LEFT JOIN landmatrix_stakeholderattributegroup AS skvf1            ON s.id = skvf1.fk_stakeholder_id AND skvf1.attributes ? 'country'",
        "LEFT JOIN landmatrix_country                   AS investor_country ON CAST(skvf1.attributes->'country' AS NUMERIC) = investor_country.id",
        "LEFT JOIN landmatrix_activityattributegroup    AS target_country   ON a.id = target_country.fk_activity_id AND target_country.attributes ? 'target_country'",
        "LEFT JOIN landmatrix_country                   AS deal_country     ON CAST(target_country.attributes->'target_country' AS NUMERIC) = deal_country.id",
    ]
    ADDITIONAL_WHERES = ["investor_country.id IS NOT NULL"]
    GROUP_BY = ['sub.target_country', 'sub.target_country_id']
    ORDER_BY = ['hectares DESC']
    LIMIT = 10


class Top10CountriesQuerySet:

    def __init__(self, get_data):
        self.get_data = get_data

    def all(self):
        output = {
            "investor_country": [],
            "target_country": [],
        }
        for c in self.get_top_10_investors(self.get_data):
            country = TransnationalDealsQuerySet.LONG_COUNTRIES.get(c['investor_country'], c['investor_country'])
            output["investor_country"].append(
                {"name": country, "slug": slugify(c['investor_country']), "hectares": c['hectares'], "id": c['investor_country_id'], "deals": c['deals']}
            )
        for c in self.get_top_10_target_countries(self.get_data):
            country = TransnationalDealsQuerySet.LONG_COUNTRIES.get(c['target_country'], c['target_country'])
            output["target_country"].append(
                {"name": country, "slug": slugify(c['target_country']), "hectares": c['hectares'], "id":c['target_country_id'], "deals": c['deals']}
            )
        return output

    def get_top_10_investors(self, get):
        queryset = Top10InvestorCountriesQuerySet(get)
        return queryset.all()

    def get_top_10_target_countries(self, get):
        queryset = Top10TargetCountriesQuerySet(get)
        return queryset.all()
