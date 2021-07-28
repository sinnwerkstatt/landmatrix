from django.db.models import Q
from graphql import GraphQLResolveInfo, FieldNode


def get_fields(info: GraphQLResolveInfo, recursive=False, exclude=None):
    if exclude is None:
        exclude = []
    fields = []
    for fnode in info.field_nodes:
        if not fnode.selection_set:
            continue
        for selection in fnode.selection_set.selections:
            if recursive:
                fields += _recursive_fieldnode(selection, exclude)
            else:
                sel = selection.name.value
                if sel not in exclude:
                    fields += [sel]
    return fields


def _recursive_fieldnode(fnode: FieldNode, exclude):
    if fnode.selection_set:
        sel_set = []
        for selection in fnode.selection_set.selections:
            sel_set += _recursive_fieldnode(selection, exclude)
        return [f"{fnode.name.value}__{sel}" for sel in sel_set if sel not in exclude]
    elif fnode.name.value not in exclude:
        return [fnode.name.value]
    return []


filter_ops = {
    "EQ": "",
    "LT": "__lt",
    "LE": "__lte",
    "GE": "__gte",
    "GT": "__gt",
    "IN": "__in",
    "CONTAINS": "__contains",
    "CONTAINED_BY": "__contained_by",
    "OVERLAP": "__overlap",
}


def parse_filters(filters):
    ret = Q()
    if not filters:
        return ret
    for filtr in filters:
        field = filtr["field"].replace(".", "__")
        op = filtr.get("operation") or "EQ"
        val = filtr["value"]
        if (
            isinstance(val, list)
            and len(val) == 1
            and op in ["EQ", "LT", "LE", "GE", "GT"]
        ):
            val = val[0]
        operation = filter_ops[op]

        filter_operation = Q(**{f"{field}{operation}": val})
        if filtr.get("allow_null"):
            filter_operation |= Q(**{f"{field}": None})
        if filtr.get("exclusion"):
            filter_operation = ~filter_operation
        ret &= filter_operation
    return ret
