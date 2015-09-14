from landmatrix.models.activity_attribute_group import ActivityAttributeGroup

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class JSONViewBase:

    BASE_FILTER_MAP = {
        "concluded": ("concluded (oral agreement)", "concluded (contract signed)"),
        "intended": ("intended (expression of interest)", "intended (under negotiation)" ),
        "failed": ("failed (contract canceled)", "failed (negotiations failed)"),
    }

    def _get_filter(self, negotiation_status, deal_scope, data_source_type):
        filter_sql = ""
        if len(deal_scope) == 0:
            # when no negotiation stati or deal scope given no deals should be shown at the public interface
            return " AND 1 <> 1 "
        if negotiation_status:
            stati = []
            for n in negotiation_status:
                stati.extend(self.BASE_FILTER_MAP.get(n))
            filter_sql += " AND LOWER(negotiation.attributes->'pi_negotiation_status') IN ('%s') " % "', '".join(stati)
        if len(deal_scope) == 1:
            filter_sql += " AND deal_scope.attributes->'deal_scope' = '%s' " % deal_scope[0]
        if data_source_type:
            filter_sql += """ AND NOT (
            SELECT ARRAY_AGG(data_source_type.attributes->'type')
            FROM %s AS data_source_type
            WHERE a.id = data_source_type.fk_activity_id AND data_source_type.attributes ? 'type'
        ) = ARRAY['Media report']""" % ActivityAttributeGroup._meta.db_table

        return filter_sql


