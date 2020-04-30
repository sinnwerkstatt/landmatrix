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


def parse_filters(filterset):
    ret = {}
    for filter in filterset["filters"]:
        k, v = filter.split("=")
        ret[k] = v
        # if not filter["operation"]:
        #     ret[f"{filter['field']}"] = filter["value"]
        # else:
        #     ret[f"{filter['field']}__gt"] = filter["value"]
    print(ret)
    return ret
