from api.query_sets.fake_query_set_with_subquery import FakeQuerySetFlat


class FilterQuerySet(FakeQuerySetFlat):
    '''
    Filter queryset simply returns a list of activity IDs that match the
    session/request object filters.

    For use with normal Django ORM querys that must be filtered.
    '''
    FIELDS = (('id', 'a.id'),)
    QUERY = """
SELECT DISTINCT
--  columns:
    %s
FROM landmatrix_activity                       AS a
--  additional joins:
%s
WHERE
    %s
--  additional where conditions:
    %s
--  filter sql:
    %s
--  group by:
%s
--  limit:
%s
"""
    APPLY_GLOBAL_FILTERS = True
