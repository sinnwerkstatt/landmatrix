from api.query_sets.fake_query_set_with_subquery import FakeQuerySetWithSubquery

from django.template.defaultfilters import slugify

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class TransnationalDealsQuerySetBase(FakeQuerySetWithSubquery):

    FIELDS = [
        ('region_id', 'sub.region_id'),
        ('region',    'sub.region'),
        ('deals',     'COUNT(DISTINCT a.activity_identifier)'),
        ('hectares',  "ROUND(SUM(CAST(REPLACE(size.attributes->'pi_deal_size', ',', '.') AS NUMERIC)))")
    ]
    GROUP_BY = ['sub.region_id', 'sub.region']

    def __init__(self, get_data):
        super().__init__(get_data)
        self.country = get_data.get("country", "")

    def all(self):
        if self.country:
            self._additional_wheres.append("%s.id = %s " % (self.country, self.COUNTRY_FIELD))
        return super().all()



class TransnationalDealsByTargetCountryQuerySet(TransnationalDealsQuerySetBase):

    SUBQUERY_FIELDS = [
        ('region_id', "deal_region.id"),
        ('region',    "deal_region.name")
    ]
    COUNTRY_FIELD = 'investor_country'
    ADDITIONAL_JOINS = [
        "LEFT JOIN landmatrix_stakeholder               AS s                ON i.fk_stakeholder_id = s.id",
        "LEFT JOIN landmatrix_stakeholderattributegroup AS skvf1            ON s.id = skvf1.fk_stakeholder_id AND skvf1.attributes ? 'country'",
        "LEFT JOIN landmatrix_country                   AS investor_country ON CAST(skvf1.attributes->'country' AS NUMERIC) = investor_country.id",
        "LEFT JOIN landmatrix_activityattributegroup    AS target_country   ON a.id = target_country.fk_activity_id AND target_country.attributes ? 'target_country'",
        "LEFT JOIN landmatrix_country                   AS deal_country     ON CAST(target_country.attributes->'target_country' AS NUMERIC) = deal_country.id",
        "LEFT JOIN landmatrix_region                    AS deal_region      ON  deal_country.fk_region_id = deal_region.id",
        "LEFT JOIN landmatrix_activityattributegroup    AS negotiation      ON a.id = negotiation.fk_activity_id AND negotiation.attributes ? 'pi_negotiation_status'"
        "LEFT JOIN landmatrix_activityattributegroup    AS deal_scope       ON a.id = deal_scope.fk_activity_id AND deal_scope.attributes ? 'deal_scope'"
    ]
    ADDITIONAL_WHERES = ["deal_region.name IS NOT NULL", "investor_country.id <> deal_country.id"]


class TransnationalDealsByInvestorCountryQuerySet(TransnationalDealsQuerySetBase):

    SUBQUERY_FIELDS = [
        ('region_id', "investor_region.id"),
        ('region',    "investor_region.name")
    ]

    COUNTRY_FIELD = 'deal_country'

    ADDITIONAL_JOINS = [
        "LEFT JOIN landmatrix_stakeholder               AS s                ON i.fk_stakeholder_id = s.id",
        "LEFT JOIN landmatrix_stakeholderattributegroup AS skvf1            ON s.id = skvf1.fk_stakeholder_id AND skvf1.attributes ? 'country'",
        "LEFT JOIN landmatrix_country                   AS investor_country ON CAST(skvf1.attributes->'country' AS NUMERIC) = investor_country.id",
        "LEFT JOIN landmatrix_region                    AS investor_region  ON investor_country.fk_region_id = investor_region.id",
        "LEFT JOIN landmatrix_activityattributegroup    AS target_country   ON a.id = target_country.fk_activity_id AND target_country.attributes ? 'target_country'",
        "LEFT JOIN landmatrix_country                   AS deal_country     ON CAST(target_country.attributes->'target_country' AS NUMERIC) = deal_country.id",
        "LEFT JOIN landmatrix_activityattributegroup    AS negotiation      ON a.id = negotiation.fk_activity_id AND negotiation.attributes ? 'pi_negotiation_status'"
        "LEFT JOIN landmatrix_activityattributegroup    AS deal_scope       ON a.id = deal_scope.fk_activity_id AND deal_scope.attributes ? 'deal_scope'"
    ]
    ADDITIONAL_WHERES = ["investor_country.name IS NOT NULL", "investor_country.id <> deal_country.id"]

class TransnationalDealsByCountryQuerySet:

    def __init__(self, get_data):
        self.get_data = get_data

    def all(self):
        return {
            'target_country': aggregate_regions(self.get_transnational_deals_by_target_country(self.get_data)),
            'investor_country': aggregate_regions(self.get_transnational_deals_by_investor_country(self.get_data))
        }

    def get_transnational_deals_by_target_country(self, get):
        queryset = TransnationalDealsByTargetCountryQuerySet(get)
        return queryset.all()

    def get_transnational_deals_by_investor_country(self, get):
        queryset = TransnationalDealsByInvestorCountryQuerySet(get)
        return queryset.all()


def aggregate_regions(t_deals):
    sum_deals, sum_hectares = 0, 0
    output = []
    for d in t_deals:
        output.append({
            "region_id": d['region_id'],
            "region": d['region'],
            "deals": d['deals'] or 0,
            "hectares": d['hectares'] or 0,
            "slug": slugify(d['region']),
        })
        sum_deals += d['deals'] or 0
        sum_hectares += float(d['hectares'] or 0)
    output.append({
        "region_id": 0,
        "region": "Total",
        "deals": sum_deals,
        "hectares": sum_hectares,
    })
    return output
