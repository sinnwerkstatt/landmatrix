from django.db import connection

from .involvement_sql import GRAPH_QUERY


class InvolvementNetwork:
    def __init__(self, include_ventures=False, max_depth=10):
        self.traveled_edges = []
        self.seen_investors = set()
        self.include_ventures = include_ventures
        self.max_depth = max_depth

    def get_new_network(self, investor_id, depth) -> list:
        with connection.cursor() as cursor:
            cursor.execute(GRAPH_QUERY, [depth, investor_id])
            for row in cursor.fetchall():
                print(row)
