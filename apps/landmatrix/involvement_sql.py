GRAPH_QUERY = """
with recursive
    search_involvements(id, down_edges, up_edges, down_path, up_path, depth)
        as (select id, children, parents, array [id], array [id], %s
            from involvements_bidi
            where id = %s
            union all

            select g.id,
                   children,
                   parents,
                   g.id || down_path,
                   up_path || g.id,
                   depth - 1
            FROM involvements_bidi g,
                 search_involvements sg
            WHERE depth > 0
              AND (
                    (g.id <> all (down_path) and g.id = any (sg.down_edges)) or
                    (g.id <> all (up_path) and g.id = any (sg.up_edges))
                )),
    involvements_bidi as
        (select i.id,
                array_remove(array_agg(distinct (a.child_investor_id)), NULL)  as children,
                array_remove(array_agg(distinct (b.parent_investor_id)), NULL) as parents
         from landmatrix_investorhull i
                  full outer join landmatrix_involvement a on i.id = a.parent_investor_id
                  full outer join landmatrix_involvement b on i.id = b.child_investor_id
                  where i.active_version_id is not null and i.deleted is false
         group by (i.id))
select depth, id, down_edges, up_edges
from search_involvements
order by (depth, id) desc;
"""

UNIDIRECTIONAL_GRAPH_QUERY = """
with recursive
    search_involvements(id, up_edges, up_path, depth)
        as (select id, parents, array [id], %s
            from involvements_bidi
            where id = %s
            union all

            select g.id,
                   parents,
                   up_path || g.id,
                   depth - 1
            FROM involvements_bidi g,
                 search_involvements sg
            WHERE depth > 0
              AND                     
                    (g.id <> all (up_path) and g.id = any (sg.up_edges))
                ),
    involvements_bidi as
        (select i.id,
                array_remove(array_agg(distinct (a.child_investor_id)), NULL)  as children,
                array_remove(array_agg(distinct (b.parent_investor_id)), NULL) as parents
         from landmatrix_investorhull i
                  full outer join landmatrix_involvement a on i.id = a.parent_investor_id
                  full outer join landmatrix_involvement b on i.id = b.child_investor_id
                  where i.active_version_id is not null and i.deleted is false
         group by (i.id))
select depth, id, up_edges
from search_involvements
order by (depth, id) desc;
"""

# TODO Later faster version requires a VIEW.
#  but how would we migrate it and keep it up2date? (when the model changes, not when the data changes)

CREATE_VIEW = """
create view involvements_bidi as
(
select i.id,
       array_remove(array_agg(distinct (a.child_investor_id)), NULL)  as children,
       array_remove(array_agg(distinct (b.parent_investor_id)), NULL) as parents
from landmatrix_investor i
         full outer join landmatrix_involvement a on i.id = a.parent_investor_id
         full outer join landmatrix_involvement b on i.id = b.child_investor_id
group by (i.id)
    );
"""

QUERY_USE_VIEW = """
with recursive
    search_involvements(id, down_edges, up_edges, down_path, up_path, depth)
        as (select id, children, parents, array [id], array [id], 15
            from involvements_bidi
            where id = 2597
            union all

            select g.id,
                   children,
                   parents,
                   down_path || g.id,
                   up_path || g.id,
                   depth - 1
            FROM involvements_bidi g,
                 search_involvements sg
            WHERE depth > 0
              AND (
                    (g.id <> all (down_path) and g.id = any (sg.down_edges)) or
                    (g.id <> all (up_path) and g.id = any (sg.up_edges))
                ))
select depth, id, down_path, up_path
from search_involvements
order by (depth, id, down_path, up_path) desc;
"""
