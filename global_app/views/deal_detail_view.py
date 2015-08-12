__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from landmatrix.models import Activity, ActivityAttributeGroup, Involvement, PrimaryInvestor, Stakeholder, StakeholderAttributeGroup
from .view_aux_functions import render_to_response

from django.views.generic import TemplateView
from django.template import RequestContext
from django.db.models import Max


class DealDetailView(TemplateView):

    template_name = 'deal-detail.html'

    def dispatch(self, request, *args, **kwargs):

        self.request = request
        deal_id = kwargs["deal_id"]

        activity = get_latest_activity(deal_id)
        attributes = get_activity_attributes(activity)

        primary_investor_ids, stakeholder_ids = get_pi_and_sh_id(activity)

        primary_investor = PrimaryInvestor.objects.filter(id__in=primary_investor_ids).last()

        sh = Stakeholder.objects.filter(id__in=stakeholder_ids).last()
        stakeholder = get_stakeholder_attributes(sh)

        context = {
            "deal": {
                'activity': activity,
                'attributes': attributes,
                'primary_investor': primary_investor,
                'stakeholder': stakeholder,
            }
        }
        return render_to_response(self.template_name, context, RequestContext(self.request))


def get_pi_and_sh_id(activity):
    queryset = Involvement.objects.select_related().filter(fk_activity=activity)
    involvements = queryset.values('fk_primary_investor_id', 'fk_stakeholder_id')
    return [i['fk_primary_investor_id'] for i in involvements], [i['fk_stakeholder_id'] for i in involvements]


def get_activity_attributes(activity):
    attributes = ActivityAttributeGroup.objects.filter(fk_activity=activity).values('attributes')
    attributes_list = [a['attributes'] for a in attributes]
    return aggregate_activity_attributes(attributes_list, {})


def aggregate_activity_attributes(attributes_list, already_set_attributes):
    if not attributes_list:
        return already_set_attributes

    for key, value in attributes_list.pop(0).items():
        already_set_attributes[key] = value

    return aggregate_activity_attributes(attributes_list, already_set_attributes)


def get_stakeholder_attributes(stakeholder):
    attributes = StakeholderAttributeGroup.objects.filter(fk_stakeholder=stakeholder).values('attributes')
    return {key: value for a in attributes for key, value in a['attributes'].items()}


def get_latest_activity(deal_id):
    version_max = _get_latest_version(deal_id)
    return Activity.objects.filter(activity_identifier=deal_id, version=version_max).last()


def _get_latest_version(deal_id):
    return Activity.objects.filter(activity_identifier=deal_id).values().aggregate(Max('version'))['version__max']


def _get_latest_stakeholder_version(deal_id):
    return Activity.objects.filter(activity_identifier=deal_id).values().aggregate(Max('version'))['version__max']

