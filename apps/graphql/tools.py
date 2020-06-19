from graphql import GraphQLResolveInfo, FieldNode


def get_fields(info: GraphQLResolveInfo, recursive=False):
    fields = []
    for fnode in info.field_nodes:
        for selection in fnode.selection_set.selections:
            if recursive:
                fields += _recursive_fieldnode(selection)
            else:
                fields += [selection.name.value]
    return fields


def _recursive_fieldnode(fnode: FieldNode):
    if fnode.selection_set:
        sel_set = []
        for selection in fnode.selection_set.selections:
            sel_set += _recursive_fieldnode(selection)
        return [f"{fnode.name.value}__{sel}" for sel in sel_set]
    else:
        return [fnode.name.value]


filter_ops = {
    "EQ": "",
    # Dont provide NE? Or do we have to? It's a "exclude" hassle
    "IN": "__in",
    "CONTAINS": "__icontains",
    "LT": "__lt",
    "LE": "__lte",
    "GE": "__gte",
    "GT": "__gt",
}


def parse_filters(filters):
    ret = {}
    for filt in filters:
        field = filt["field"].replace(".", "__")
        val = filt["value"]
        if field not in ["IN", "CONTAINS"] and isinstance(val, list) and len(val) == 1:
            val = val[0]
        operation = filter_ops[filt["operation"]]
        ret[f"{field}{operation}"] = val
    return ret
