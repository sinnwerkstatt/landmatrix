from api.query_sets.fake_query_set_with_subquery import FakeQuerySetWithSubquery

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class AgriculturalProduceQuerySet(FakeQuerySetWithSubquery):
    # TODO: I think this query is broken

    FIELDS = [
        ('agricultural_produce', 'sub.agricultural_produce'),
        ('deals',      'COUNT(DISTINCT a.activity_identifier)'),
        ('hectares',   "ROUND(SUM(a.deal_size))"),
    ]
    SUBQUERY_FIELDS = [
        ('agricultural_produce', """CASE
            WHEN (
                SELECT COUNT(DISTINCT ap.name)
                FROM landmatrix_crop                   AS c
                JOIN landmatrix_agriculturalproduce    AS ap ON c.fk_agricultural_produce_id = ap.id
                JOIN landmatrix_activityattribute      AS kv
                    ON a.id = kv.fk_activity_id
                    AND kv.name = 'crops'
                    AND CAST(kv.value AS NUMERIC) = c.id
            ) > 1 THEN 'Multiple use'
            ELSE (
                SELECT ap.name
                FROM landmatrix_crop                   AS c
                JOIN landmatrix_agriculturalproduce    AS ap ON c.fk_agricultural_produce_id = ap.id
                JOIN landmatrix_activityattribute      AS kv
                    ON a.id = kv.fk_activity_id
                    AND kv.name = 'crops'
                    AND CAST(kv.value AS NUMERIC) = c.id
                LIMIT 1
            )
        END"""),
    ]
    ADDITIONAL_JOINS = [
        #"LEFT JOIN landmatrix_activityattribute         AS intention        ON a.id = intention.fk_activity_id AND intention.name = 'intention'",
        "LEFT JOIN landmatrix_activityattribute         AS target_country   ON a.id = target_country.fk_activity_id AND target_country.name = 'target_country'",
        "LEFT JOIN landmatrix_country                   AS deal_country     ON target_country.name = 'target_country' AND CAST(target_country.value AS NUMERIC) = deal_country.id",
        "LEFT JOIN landmatrix_region                    AS deal_region      ON deal_country.fk_region_id = deal_region.id",
    ]
    GROUP_BY = ['sub.agricultural_produce']
    ORDER_BY = ['sub.agricultural_produce']


    def __init__(self, request, region_ids):
        super().__init__(request)
        self.region_ids = region_ids

    def all(self):
        if self.region_ids:
            self._additional_wheres = ["deal_region.id IN (%s)" % ",".join(self.region_ids)]
        return super().all()


class AllAgriculturalProduceQuerySet:
    # TODO: don't hardcode regions here, since we have a model for that
    REGIONS = {
        'america': ['21', '419'],
        'africa':  ["2"],
        'asia':    ["142"],
        'oceania': ["9"],
        'europe':  ["150"],
        'overall': None
    }

    def __init__(self, get_data):
        self.get_data = get_data

    def all(self):
        output = []
        for region, value in self.REGIONS.items():
            ap_region = {
                "food_crop": 0,
                "non_food": 0,
                "flex_crop": 0,
                "multiple_use": 0,
            }
            hectares = {
                "food_crop": 0,
                "non_food": 0,
                "flex_crop": 0,
                "multiple_use": 0,
            }
            ap_list = self.get_agricultural_produces(self.get_data, value)
            available_sum, not_available_sum = self.calculate_sums(ap_list)

            for ap in ap_list:
                if ap['agricultural_produce']:
                    ap_name = ap['agricultural_produce'].lower().replace(" ", "_").replace("-", "_")
                    ap_region[ap_name] = round(float(ap['hectares'])/available_sum*100)
                    hectares[ap_name] = ap['hectares']

            output.append({
                "region": region,
                "available": available_sum,
                "not_available": not_available_sum,
                "agricultural_produce": ap_region,
                "hectares": hectares,
            })
        return output

    def calculate_sums(self, ap_list):
        available_sum, not_available_sum = 0, 0
        for ap in ap_list:
            if ap['agricultural_produce']:
                available_sum += float(ap['hectares'])
            else:
                not_available_sum += float(ap['hectares'])
        return available_sum, not_available_sum

    def get_agricultural_produces(self, get, region_ids):
        queryset = AgriculturalProduceQuerySet(get, region_ids)
        sanitized_values = [
            {
                'agricultural_produce': item['agricultural_produce'] or 0.0,
                'deals': item['deals'] or 0,
                'hectares': item['hectares'] or 0.0,
            }
            for item in queryset.all()
        ]
        return sanitized_values
