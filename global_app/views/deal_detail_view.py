__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from landmatrix.models import Activity, ActivityAttributeGroup
from .view_aux_functions import render_to_response

from django.views.generic import TemplateView
from django.template import RequestContext
from django.db.models import Max


class DealDetailView(TemplateView):

    template_name = 'deal-detail.html'

    def dispatch(self, request, *args, **kwargs):
        from pprint import pprint
        self.request = request
        deal_id = kwargs["deal_id"]

        activity = get_latest_activity(deal_id)
        attributes = get_activity_attributes(activity)

        context = {
            "deal": {
                'activity': activity,
                'attributes': attributes
            }
        }
        return render_to_response(self.template_name, context, RequestContext(self.request))


def get_activity_attributes(activity):
    attributes = ActivityAttributeGroup.objects.filter(fk_activity=activity).values('attributes')
    return [a['attributes'] for a in attributes]


def get_latest_activity(deal_id):
    version_max = _get_latest_version(deal_id)
    return Activity.objects.filter(activity_identifier=deal_id, version=version_max).last()


def _get_latest_version(deal_id):
    return Activity.objects.filter(activity_identifier=deal_id).values().aggregate(Max('version'))['version__max']