from api.query_sets.fake_query_set_with_subquery import FakeQuerySetFlat
from django.core.urlresolvers import reverse

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class InvestorCountrySummariesQuerySet(FakeQuerySetFlat):

    fields = [
        ('country_id', 'investor_country.id'),
        ('country',    'investor_country.name'),
        ('region',     'investor_region.name'),
        ('lat',        'investor_country.point_lat'),
        ('lon',        'investor_country.point_lon'),
        ('deals',      'COUNT(DISTINCT a.activity_identifier)'),
        ('deal_scope', "deal_scope.attributes->'deal_scope'")
    ]
    _additional_joins = [
        "LEFT JOIN landmatrix_activityattributegroup    AS negotiation      ON a.id = negotiation.fk_activity_id AND negotiation.attributes ? 'pi_negotiation_status'"
        "LEFT JOIN landmatrix_activityattributegroup    AS deal_scope       ON a.id = deal_scope.fk_activity_id AND deal_scope.attributes ? 'deal_scope'"
        "LEFT JOIN landmatrix_stakeholder               AS s                ON i.fk_stakeholder_id = s.id",
        "LEFT JOIN landmatrix_stakeholderattributegroup AS skvf1            ON s.id = skvf1.fk_stakeholder_id AND skvf1.attributes ? 'country'",
        "LEFT JOIN landmatrix_country                   AS investor_country ON CAST(skvf1.attributes->'country' AS NUMERIC) = investor_country.id",
        "LEFT JOIN landmatrix_region                    AS investor_region  ON investor_country.fk_region_id = investor_region.id",
        "LEFT JOIN landmatrix_activityattributegroup    AS target_country   ON a.id = target_country.fk_activity_id AND target_country.attributes ? 'target_country'",
        "LEFT JOIN landmatrix_country                   AS deal_country     ON CAST(target_country.attributes->'target_country' AS NUMERIC) = deal_country.id",
    ]
    _group_by = ["investor_country.id, investor_region.name, deal_scope.attributes->'deal_scope'"]

    def all(self):
        countries_summary = super().all()

        countries = {}
        for c in countries_summary:
            if not c['country_id']: continue
            country = countries.get(c['country_id'], {"domestic": 0, "transnational": 0})
            country.update(self.to_json_record(c, country))
            countries.update({c['country_id']: country})

        return [v for k,v in countries.items()]

    def to_json_record(self, c, country):
        c['name'] = c['country']
        c["country_slug"] =c['country'].lower().replace(" ", "-")
        c["region_slug"] =c['region'].lower().replace(" ", "-")
        c['url'] = reverse("table_list", kwargs={"group": "by-target-country", "list": c['country'].lower().replace(" ", "-")})
        c[c['deal_scope']] = c['deals'] + country.get(c['deal_scope'], 0)
        c['deals'] = c['deals'] + country.get("deals", 0)

        return c
