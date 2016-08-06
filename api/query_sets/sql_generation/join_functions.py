__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from landmatrix.models.activity_attribute_group import ActivityAttribute


def get_join_columns(columns, group, group_value):
    if group_value and group not in columns:
        join_columns = columns[:]
        join_columns.append(group)
    else:
        join_columns = columns
    return join_columns


def join(table_or_model, alias, on):
    if not isinstance(table_or_model, str):
        table_or_model = table_or_model._meta.db_table
    return "LEFT JOIN %-36s AS %-21s ON %s " % (table_or_model, alias, on)


def join_expression(table_or_model, alias, local_field, foreign_field='id'):
    return join(
        table_or_model, alias,
        "%s = %s.%s"   % (local_field, alias, foreign_field)
    )


def local_table_alias(model):
    if model == ActivityAttribute: return 'a'
    else: raise RuntimeError('Model not recognized: '+str(model))


def join_attributes(alias, attribute='', attributes_model=ActivityAttribute, attribute_field='fk_activity_id'):
    if not attribute: attribute = alias
    return join(
        attributes_model, alias,
        "%s.id = %s.%s AND %s.name = '%s'" % (
            local_table_alias(attributes_model),
            alias,
            attribute_field,
            alias,
            attribute
        )
    )


def join_activity_attributes(alias, attribute):
    return join(
        ActivityAttribute,
        alias,
        on="a.activity_identifier = %s.activity_identifier AND %s.name = '%s'" % (
            alias,
            alias,
            attribute
        )
    )
