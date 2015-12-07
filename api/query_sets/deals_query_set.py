from api.query_sets.fake_query_set_with_subquery import FakeQuerySetFlat
import timeit

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class DealsQuerySet(FakeQuerySetFlat):

    BASE_FILTER_MAP = {
        "concluded": ("concluded (oral agreement)", "concluded (contract signed)"),
        "intended": ("intended (expression of interest)", "intended (under negotiation)" ),
        "failed": ("failed (contract canceled)", "failed (negotiations failed)"),
    }

    FIELDS = [
        ('point_lat', "location.attributes->'point_lat'"),
        ('point_lon', "location.attributes->'point_lon'"),
        ('intention', "NULLIF(ARRAY_TO_STRING(ARRAY_AGG(DISTINCT intention.attributes->'intention'), ', '), '')")
    ]
    ADDITIONAL_JOINS = [
        "LEFT JOIN landmatrix_activityattributegroup    AS location         ON a.id = location.fk_activity_id AND location.attributes ? 'point_lat' AND location.attributes ? 'point_lon'",
        "LEFT JOIN landmatrix_activityattributegroup    AS intention        ON a.id = intention.fk_activity_id AND intention.attributes ? 'intention'"
    ]
    ADDITIONAL_WHERES = ["location.attributes ? 'point_lat' AND location.attributes ? 'point_lon'"]
    GROUP_BY = ['location.attributes']

    def __init__(self, get_data):
        if not 'deal_scope' in get_data:
            get_data = get_data.copy()
            get_data.setlist('deal_scope', ['domestic', 'transnational'])
        super().__init__(get_data)
        self._set_limit(get_data.get('limit', None))
        self._set_investor_country(get_data.get('investor_country', None))
        self._set_investor_region(get_data.get('investor_region', None))
        self._set_target_country(get_data.get('target_country', None))
        self._set_target_region(get_data.get('target_region', None))
        if get_data.get('window'):
            lat_min, lat_max, lon_min, lon_max = get_data.get('window').split(',')
            self._set_window(lat_min, lat_max, lon_min, lon_max)

    def all(self):
        start_time = timeit.default_timer()

        output = super().all()

        if self.DEBUG:
            print('Query time:', timeit.default_timer() - start_time)

        return output

    def _set_limit(self, limit):
        self._limit = limit

    def _set_investor_country(self, country_id):
        if not country_id: return
        self._additional_joins = add_to_list_if_not_present(
            self._additional_joins, [
                "LEFT JOIN landmatrix_investorventureinvolvement AS ivi             ON ivi.fk_venture_id = operational_stakeholder.id",
                "LEFT JOIN landmatrix_investor                  AS stakeholder      ON ivi.fk_investor_id = stakeholder.id",
        ])
        self._additional_wheres = add_to_list_if_not_present(
            self._additional_wheres, [
                "stakeholder.fk_country_id = %s" % country_id
        ])

    def _set_investor_region(self, region_id):
        if not region_id: return
        self._additional_joins = add_to_list_if_not_present(
            self._additional_joins, [
                "LEFT JOIN landmatrix_investorventureinvolvement AS ivi             ON ivi.fk_venture_id = operational_stakeholder.id",
                "LEFT JOIN landmatrix_investor                  AS stakeholder      ON ivi.fk_investor_id = stakeholder.id",
                "LEFT JOIN landmatrix_country                   AS investor_country ON stakeholder.fk_country_id = investor_country.id",
        ])
        self._additional_wheres = add_to_list_if_not_present(
            self._additional_wheres, [
                "investor_country.fk_region_id = " + region_id
        ])

    def _set_target_country(self, country_id):
        if not country_id: return
        self._additional_joins = add_to_list_if_not_present(
            self._additional_joins, [
                "LEFT JOIN landmatrix_activityattributegroup    AS target_country   ON a.id = target_country.fk_activity_id AND target_country.attributes ? 'target_country'",
        ])
        self._additional_wheres = add_to_list_if_not_present(
            self._additional_wheres, [
                "target_country.attributes->'target_country' = '%s'" % country_id
        ])

    def _set_target_region(self, region_id):
        if not region_id: return
        self._additional_joins = add_to_list_if_not_present(
            self._additional_joins, [
                "LEFT JOIN landmatrix_activityattributegroup    AS target_country   ON a.id = target_country.fk_activity_id AND target_country.attributes ? 'target_country'",
                "LEFT JOIN landmatrix_country                   AS deal_country     ON CAST(target_country.attributes->'target_country' AS NUMERIC) = deal_country.id"
        ])
        self._additional_wheres = add_to_list_if_not_present(
            self._additional_wheres, [
                "deal_country.fk_region_id = " + region_id
        ])

    def _set_window(self, lat_min, lat_max, lon_min, lon_max):
        # respect the 180th meridian
        if lon_min > lon_max: lon_max, lon_min = lon_min, lon_max
        self._additional_wheres = add_to_list_if_not_present(
            self._additional_wheres, [
                "CAST(location.attributes->'point_lat' AS NUMERIC) >= " + lat_min,
                "CAST(location.attributes->'point_lat' AS NUMERIC) <= " + lat_max,
                "CAST(location.attributes->'point_lon' AS NUMERIC) >= " + lon_min,
                "CAST(location.attributes->'point_lon' AS NUMERIC) <= " + lon_max,
        ])

    def _set_negotiation_status(self, negotiation_status):
        if not negotiation_status: return
        self._additional_joins = add_to_list_if_not_present(
            self._additional_joins, [
                "LEFT JOIN landmatrix_activityattributegroup    AS negotiation      ON a.id = negotiation.fk_activity_id AND negotiation.attributes ? 'pi_negotiation_status'"
        ])
        stati = []
        for n in negotiation_status:
            stati.extend(self.BASE_FILTER_MAP.get(n))

        self._additional_wheres = add_to_list_if_not_present(
            self._additional_wheres, [
                "LOWER(negotiation.attributes->'pi_negotiation_status') IN ('%s') " % "', '".join(stati)
        ])


def add_to_list_if_not_present(old_list, additional_elements):
    for element in additional_elements:
        if not element in old_list:
            old_list = old_list + [element]
    return old_list