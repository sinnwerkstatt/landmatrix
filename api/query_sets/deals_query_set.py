__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from api.query_sets.fake_query_set import FakeQuerySet


class DealsQuerySet(FakeQuerySet):

    BASE_FILTER_MAP = {
        "concluded": ("concluded (oral agreement)", "concluded (contract signed)"),
        "intended": ("intended (expression of interest)", "intended (under negotiation)" ),
        "failed": ("failed (contract canceled)", "failed (negotiations failed)"),
    }

    fields = [
        ('point_lat', "location.attributes->'point_lat'"),
        ('point_lon', "location.attributes->'point_lon'"),
        ('intention', "intention.attributes->'intention'")
    ]

    QUERY = """
SELECT DISTINCT
    %s
FROM landmatrix_activity                    AS a
LEFT JOIN landmatrix_activityattributegroup    AS location         ON a.id = location.fk_activity_id AND location.attributes ? 'point_lat' AND location.attributes ? 'point_lon'
LEFT JOIN landmatrix_activityattributegroup    AS intention        ON a.id = intention.fk_activity_id AND intention.attributes ? 'intention'
LEFT JOIN landmatrix_activityattributegroup    AS bf               ON a.id = bf.fk_activity_id AND bf.attributes ? 'pi_deal'
LEFT JOIN landmatrix_involvement               AS i                ON i.fk_activity_id = a.id
LEFT JOIN landmatrix_primaryinvestor           AS pi               ON i.fk_primary_investor_id = pi.id
-- additional joins:
-- if filtering by implementation status
--    LEFT JOIN landmatrix_activityattributegroup    AS implementation   ON a.id = implementation.fk_activity_id AND implementation.attributes ? 'pi_implementation_status'
%s
WHERE
    a.version = (
        SELECT MAX(version) FROM landmatrix_activity AS amax
        WHERE amax.activity_identifier = a.activity_identifier AND amax.fk_status_id IN (2, 3, 4)
    )
    AND a.fk_status_id IN (2, 3)
    AND bf.attributes->'pi_deal' = 'True'
    AND pi.version = (
        SELECT MAX(version) FROM landmatrix_primaryinvestor AS pimax
        WHERE pimax.primary_investor_identifier = pi.primary_investor_identifier AND pimax.fk_status_id IN (2, 3, 4)
    )
    AND pi.fk_status_id IN (2, 3)
-- additional where conditions:
    %s
-- filter sql:
    %s
"""
    _additional_joins = []
    _additional_wheres = []

    def __init__(self):
        super().__init__('')

    def set_limit(self, limit):
        self.limit = limit

    def set_investor_country(self, country_id):
        if not country_id: return
        add_to_list_if_not_present(
            self._additional_joins, [
                "LEFT JOIN landmatrix_stakeholder               AS s                ON i.fk_stakeholder_id = s.id",
                "LEFT JOIN landmatrix_stakeholderattributegroup AS skvf1            ON s.id = skvf1.fk_stakeholder_id AND skvf1.attributes ? 'country'",
        ])
        add_to_list_if_not_present(
            self._additional_wheres, [
                "skvf1.attributes->'country' = " + country_id
        ])

    def set_investor_region(self, region_id):
        if not region_id: return
        add_to_list_if_not_present(
            self._additional_joins, [
                "LEFT JOIN landmatrix_stakeholder               AS s                ON i.fk_stakeholder_id = s.id",
                "LEFT JOIN landmatrix_stakeholderattributegroup AS skvf1            ON s.id = skvf1.fk_stakeholder_id AND skvf1.attributes ? 'country'",
                "LEFT JOIN landmatrix_country                   AS investor_country ON CAST(skvf1.attributes->'country' AS NUMERIC) = investor_country.id",
        ])
        add_to_list_if_not_present(
            self._additional_wheres, [
                "investor_country.fk_region_id = " + region_id
        ])

    def set_target_country(self, country_id):
        if not country_id: return
        add_to_list_if_not_present(
            self._additional_joins, [
                "LEFT JOIN landmatrix_activityattributegroup    AS target_country   ON a.id = target_country.fk_activity_id AND target_country.attributes ? 'target_country'",
        ])
        add_to_list_if_not_present(
            self._additional_wheres, [
                "target_country.attributes->'target_country' = " + country_id
        ])

    def set_target_region(self, region_id):
        if not region_id: return
        add_to_list_if_not_present(
            self._additional_joins, [
                "LEFT JOIN landmatrix_activityattributegroup    AS target_country   ON a.id = target_country.fk_activity_id AND target_country.attributes ? 'target_country'",
                "LEFT JOIN landmatrix_country                   AS deal_country     ON CAST(target_country.attributes->'target_country' AS NUMERIC) = deal_country.id"
        ])
        add_to_list_if_not_present(
            self._additional_wheres, [
                "deal_country.fk_region_id = " + region_id
        ])

    def set_window(self, lat_min, lat_max, lon_min, lon_max):
        # respect the 180th meridian
        if lon_min > lon_max: lon_max, lon_min = lon_min, lon_max
        add_to_list_if_not_present(
            self._additional_wheres, [
                "CAST(location.attributes->'point_lat' AS NUMERIC) >= " + lat_min,
                "CAST(location.attributes->'point_lat' AS NUMERIC) <= " + lat_max,
                "CAST(location.attributes->'point_lon' AS NUMERIC) >= " + lon_min,
                "CAST(location.attributes->'point_lon' AS NUMERIC) <= " + lon_max,
        ])

    def set_negotiation_status(self, negotiation_status):
        if not negotiation_status: return
        add_to_list_if_not_present(
            self._additional_joins, [
                "LEFT JOIN landmatrix_activityattributegroup    AS negotiation      ON a.id = negotiation.fk_activity_id AND negotiation.attributes ? 'pi_negotiation_status'"
        ])
        stati = []
        for n in negotiation_status:
            stati.extend(self.BASE_FILTER_MAP.get(n))

        add_to_list_if_not_present(
            self._additional_wheres, [
                "LOWER(negotiation.attributes->'pi_negotiation_status') IN ('%s') " % "', '".join(stati)
        ])

    def all(self):
        if self.limit:
            self._filter_sql += 'LIMIT %s' % self.limit

        print(self.sql_query())

        return super().all()

    def columns(self):
        return ",\n    ".join([definition+" AS "+alias for alias, definition in self.fields])

    def additional_joins(self):
        return "\n".join(self._additional_joins)

    def additional_wheres(self):
        return 'AND ' + "\n    AND ".join(self._additional_wheres) if self._additional_wheres else ''

    def sql_query(self):
        return self.QUERY % (self.columns(), self.additional_joins(), self.additional_wheres(), self._filter_sql)


def add_to_list_if_not_present(old_list, additional_elements):
    for element in additional_elements:
        if not element in old_list:
            old_list.append(element)