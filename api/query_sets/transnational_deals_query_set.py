__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from api.query_sets.fake_query_set import FakeQuerySet

from django.template.defaultfilters import slugify
from itertools import islice

class TransnationalDealsQuerySet(FakeQuerySet):

    LONG_COUNTRIES = {
        'United States of America' : 'Usa*',
        'United Kingdom of Great Britain and Northern Ireland' : 'Uk*',
        'China, Hong Kong Special Administrative Region' : 'China, Hong Kong*',
        'China, Macao Special Administrative Region': 'China, Macao*',
        'Lao People\'s Democratic Republic' : 'Laos*',
        'United Republic of Tanzania' : 'Tanzania*',
        'Democratic Republic of the Congo' : 'DRC*',
        'Bolivia (Plurinational State of)' : 'Bolivia*',
        'The Former Yugoslav Republic of Macedonia': 'Macedonia*',
        'Venezuela (Bolivarian Republic of)': 'Venezuela*',
        'Republic of Moldova': 'Moldova*',
        'United Arab Emirates': 'Arab Emirates*',
        'Solomon Islands': 'Solomon Iss*',
        'Russian Federation': 'Russian Fed*',
        'Dominican Republic': 'Dominican Rep*',
        'Papua New Guinea': 'Papua New*',
        'Democratic People\'s Republic of Korea': 'North Korea*',
        'United States Virgin Islands': 'Virgin Iss*',
        'Iran (Islamic Republic of)': 'Iran*',
        'Syrian Arab Republic': 'Syria*',
        'Republic of Korea': 'South Korea*',
        'C\xf4te d\'Ivoire': 'Cote d\'Ivoire',
        'British Virgin Islands': 'British Virgin Iss*',
    }

    fields = [
        ('target_country',   'target_country'),
        ('investor_country', 'investor_country'),
    ]

    QUERY = """
SELECT DISTINCT
    CONCAT(deal_region.id, '.', deal_country.name, '#!#', deal_country.id) AS target_country,
    ARRAY_AGG(DISTINCT CONCAT(investor_region.id, '.', investor_country.name,  '#!#', investor_country.id)) AS investor_country
FROM landmatrix_activity                       AS a
JOIN      landmatrix_status                                        ON landmatrix_status.id = a.fk_status_id
LEFT JOIN landmatrix_involvement               AS i                ON i.fk_activity_id = a.id
LEFT JOIN landmatrix_stakeholder               AS s                ON i.fk_stakeholder_id = s.id
LEFT JOIN landmatrix_primaryinvestor           AS pi               ON i.fk_primary_investor_id = pi.id
LEFT JOIN landmatrix_status                    AS pi_st            ON pi.fk_status_id = pi_st.id
LEFT JOIN landmatrix_stakeholderattributegroup AS skvf1            ON s.id = skvf1.fk_stakeholder_id AND skvf1.attributes ? 'country'
LEFT JOIN landmatrix_country                   AS investor_country ON CAST(skvf1.attributes->'country' AS NUMERIC) = investor_country.id
LEFT JOIN landmatrix_region                    AS investor_region  ON investor_country.fk_region_id = investor_region.id
LEFT JOIN landmatrix_activityattributegroup    AS intention        ON a.id = intention.fk_activity_id AND intention.attributes ? 'intention'
LEFT JOIN landmatrix_activityattributegroup    AS target_country   ON a.id = target_country.fk_activity_id AND target_country.attributes ? 'target_country'
LEFT JOIN landmatrix_country                   AS deal_country     ON CAST(target_country.attributes->'target_country' AS NUMERIC) = deal_country.id
LEFT JOIN landmatrix_region                    AS deal_region      ON  deal_country.fk_region_id = deal_region.id
LEFT JOIN landmatrix_activityattributegroup    AS negotiation      ON a.id = negotiation.fk_activity_id AND negotiation.attributes ? 'pi_negotiation_status'
LEFT JOIN landmatrix_activityattributegroup    AS implementation   ON a.id = implementation.fk_activity_id AND implementation.attributes ? 'pi_implementation_status'
LEFT JOIN landmatrix_activityattributegroup    AS bf               ON a.id = bf.fk_activity_id AND bf.attributes ? 'pi_deal'
LEFT JOIN landmatrix_activityattributegroup    AS size             ON a.id = size.fk_activity_id AND size.attributes ? 'pi_deal_size'
LEFT JOIN landmatrix_activityattributegroup    AS deal_scope       ON a.id = deal_scope.fk_activity_id AND deal_scope.attributes ? 'deal_scope'
WHERE
    a.version = (
        SELECT MAX(version) FROM landmatrix_activity AS amax
        WHERE amax.activity_identifier = a.activity_identifier AND amax.fk_status_id IN (2, 3, 4)
    )
    AND a.fk_status_id IN (2, 3)
    AND bf.attributes->'pi_deal' = 'True'
    AND pi.version = (
        SELECT MAX(version) FROM landmatrix_primaryinvestor AS amax
        WHERE amax.primary_investor_identifier = pi.primary_investor_identifier AND amax.fk_status_id IN (2, 3, 4)
    )
    AND pi_st.name IN ('active', 'overwritten')
    %s
    AND investor_country.id <> deal_country.id
GROUP BY target_country
"""

    def set_regions(self, regions):
        self.regions = regions

    def shorten_country(self, country):
            country_parts = country.split(".")
            country_region = country_parts[0]
            if country_region in self.regions:
                country_region = -1
            return "%s.%s" % (country_region, self.LONG_COUNTRIES.get(country_parts[1], country_parts[1]))

    def all(self):
        from collections import OrderedDict


        region_sql = "AND deal_region.id in (%s) " % ", ".join(self.regions) if self.regions else ''
        self._filter_sql += region_sql

        t_deals = FakeQuerySet.all(self)

        countries = {}
        for d in t_deals:
            target_country = d['target_country']
#            print(d)
            target_countries = []
#            print('target_country', target_country)
            target_countries.append({
                "name": self.shorten_country(target_country.split("#!#")[0]),
                "id": target_country.split("#!#")[1],
                "slug": slugify(target_country.split("#!#")[0].split(".")[1])
            })

            for c in d['investor_country']:
                country = self.shorten_country(c.split("#!#")[0])
                countries[country] = {
                    "name": country,
                    "id": c.split("#!#")[1] ,
                    "size": 1,
                    "imports": [dcountry["name"] for dcountry in target_countries],
                    "slug": slugify(c.split("#!#")[0].split(".")[1])
                }

            for target_country in target_countries:
                if not target_country["name"] in countries:
                    countries[target_country["name"]] = {
                        "name": target_country["name"],
                        "id": target_country["id"],
                        "size": 1,
                        "imports": [] if not target_country["name"] in countries or not 'imports' in countries[target_country["name"]] else countries[target_country["name"]]['imports'],
                        "slug": target_country["slug"]
                    }

        my_countries = {}
        for d in t_deals:
            my_target_country = d['target_country']
            country = {
                'name': self.shorten_country(my_target_country.split("#!#")[0]),
                'id':   my_target_country.split("#!#")[1],
                'slug': slugify(my_target_country.split("#!#")[0].split(".")[1]),
                'size': 1,
                'imports': [ self.shorten_country(dcountry.split("#!#")[0]) for dcountry in d['investor_country'] ]
            }
            my_countries[self.shorten_country(my_target_country.split("#!#")[0])] = OrderedDict(sorted(country.items()))

        countries = OrderedDict(sorted(countries.items(), key=lambda t: t[1]['id']))
        my_countries = OrderedDict(sorted(my_countries.items(), key=lambda t: t[1]['id']))

        print(list(islice(countries.items(), 0, 4)))
        print(list(islice(my_countries.items(), 0, 4)))

        #return countries # list(islice(countries.items(), 0, 4)) # countries
        return my_countries

def original_sorting_order(index):
    order = { 'imports': 1, 'slug': 2, 'name': 3, 'size': 4, 'id': 5}
    return order[index]
