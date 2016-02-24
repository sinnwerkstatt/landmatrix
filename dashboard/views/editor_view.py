from django.shortcuts import redirect
from django.template.context import RequestContext
from django.conf import settings
from django.utils.datastructures import MultiValueDict
from django.views.generic import TemplateView
import json

from dashboard.views.changeset_protocol import ChangesetProtocol
from global_app.views.view_aux_functions import render_to_response
from landmatrix.models.activity import Activity

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class EditorView(TemplateView):

    template_name = 'dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return self.render_authenticated_user(request)
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    def render_authenticated_user(self, request):
        csp = ChangesetProtocol()
        data = {
            "a_changesets": ["updates", "deletes", "inserts"],
            "sh_changesets": ["deletes"],
        }
        request.POST = MultiValueDict({"data": [json.dumps(data)]})
        response = csp.dispatch(request, action="dashboard")
        response = json.loads(response.content.decode())
        public = get_public_deal_count()
        overall = get_overall_deal_count()
        data = {
            "statistics": {
                "overall_deal_count": overall,
                "public_deal_count": public,
                "not_public_deal_count": overall-public
            },
            "view": "dashboard",
            "latest_added": response["latest_added"],
            "latest_modified": response["latest_modified"],
            "latest_deleted": response["latest_deleted"],
            "manage": response["manage"],
            "feedbacks": response["feedbacks"],
        }
        return render_to_response(self.template_name, data, RequestContext(request))


def get_overall_deal_count():
    return Activity.objects.filter(fk_status__name__in=('active', 'overwritten')).values('activity_identifier').distinct().count()


def get_public_deal_count():
    from django.db import connection

    cursor = connection.cursor()
    cursor.execute("""
SELECT COUNT(DISTINCT a.activity_identifier)
FROM landmatrix_activity AS a
JOIN landmatrix_status AS st ON a.fk_status_id = st.id
LEFT JOIN landmatrix_activityattributegroup AS a5 ON a.id = a5.fk_activity_id AND a5.attributes ? 'production_size'
LEFT JOIN landmatrix_activityattributegroup AS a4 ON a.id = a4.fk_activity_id AND a4.attributes ? 'contract_size'
LEFT JOIN landmatrix_activityattributegroup AS a6 ON a.id = a6.fk_activity_id AND a6.attributes ? 'intended_size'
LEFT JOIN landmatrix_activityattributegroup AS a3 ON a.id = a3.fk_activity_id AND a3.attributes ? 'not_public'
LEFT JOIN landmatrix_activityattributegroup AS a2 ON a.id = a2.fk_activity_id AND a2.attributes ? 'negotiation_status'
LEFT JOIN landmatrix_activityattributegroup AS a1 ON a.id = a1.fk_activity_id AND a1.attributes ? 'implementation_status'
WHERE a.fk_status_id = st.id
AND st.name IN ('active', 'overwritten')
AND (CAST(a5.attributes->'production_size' AS NUMERIC) >= 200 OR (a5.attributes->'production_size') IS NULL)
AND (CAST(a4.attributes->'contract_size' AS NUMERIC) >= 200 OR (a4.attributes->'contract_size') IS NULL)
AND ((a4.attributes->'contract_size') IS NULL
    AND ((a5.attributes->'production_size') IS NULL)
    AND CAST(a6.attributes->'intended_size' AS NUMERIC) >= 200 OR (a6.attributes->'intended_size') IS NULL
)
AND (a3.attributes->'not_public' NOT IN ('True', 'on') OR (a3.attributes->'not_public') IS NULL)
AND (
    a2.attributes->'negotiation_status' IN ('Oral Agreement', 'Contract signed')
    AND a2.date >= '2000-01-01'
    OR (a2.attributes->'negotiation_status') IS NULL
)
AND (
    a1.attributes->'implementation_status' <> 'Project abandoned'
    OR (a1.attributes->'implementation_status') IS NULL
);
""")
    row = cursor.fetchone()
    return row[0] if row else 0



