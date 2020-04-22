from graphql import GraphQLResolveInfo


def get_fields(info: GraphQLResolveInfo):
    fields = set()
    for fnode in info.field_nodes:
        fields.update({f.name.value for f in fnode.selection_set.selections})
    return list(fields)


# from typing import List
#
# from graphql import GraphQLResolveInfo, FieldNode
#
#
# def get_fields(info: GraphQLResolveInfo) -> list:
#     fields = set()
#     # fields = [x for x in recparse(info.field_nodes)]
#     for fnode in info.field_nodes:
#         print({f.name.value for f in fnode.selection_set.selections})
#         for sel in fnode.selection_set.selections:
#             print(parse_selection_set(sel.selection_set))
#             print(sel.name.value)
#         fields.update({f.name.value for f in fnode.selection_set.selections})
#     print(fields)
#     return list(fields)
#
#
# def parse_selection_set(selection_set):
#     if not selection_set:
#         return []
#     return [x.name.value for x in selection_set.selections]
#
# def recparse(field_nodes: List[FieldNode]):
#     for node in field_nodes:
#         for selection in node.selection_set.selections:
#             yield selection.name.value
#             yield list(recparse(selection))
