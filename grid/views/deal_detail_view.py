from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse

from grid.forms.change_deal_employment_form import ChangeDealEmploymentForm
from grid.forms.change_deal_general_form import ChangeDealGeneralForm
from grid.forms.deal_data_source_form import PublicViewDealDataSourceFormSet, DealDataSourceForm
from grid.forms.deal_former_use_form import DealFormerUseForm
from grid.forms.deal_gender_related_info_form import DealGenderRelatedInfoForm
from grid.forms.deal_local_communities_form import DealLocalCommunitiesForm
from grid.forms.deal_produce_info_form import PublicViewDealProduceInfoForm
from grid.forms.deal_spatial_form import PublicViewDealSpatialForm
from grid.forms.deal_water_form import DealWaterForm
from grid.forms.operational_stakeholder_form import OperationalStakeholderForm
from grid.views.save_deal_view import name_of_form, create_attribute_group
from grid.views.view_aux_functions import render_to_string, render_to_response

from landmatrix.models import Deal
from landmatrix.models.activity import Activity
from landmatrix.models.country import Country
from landmatrix.models.deal_history import DealHistoryItem

from django.db.models import Max

from django.views.generic import TemplateView
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

FORMS = [
    ("spatial_data", PublicViewDealSpatialForm),
    ("general_information", ChangeDealGeneralForm),
    ("employment", ChangeDealEmploymentForm),
    ("investor_info", OperationalStakeholderForm),
    ("data_sources", PublicViewDealDataSourceFormSet),
    ("local_communities", DealLocalCommunitiesForm),
    ("former_use", DealFormerUseForm),
    ("produce_info", PublicViewDealProduceInfoForm),
    ("water", DealWaterForm),
    ("gender-related_info", DealGenderRelatedInfoForm),
]


class DealDetailView(TemplateView):

    template_name = 'deal-detail.html'

    def dispatch(self, request, *args, **kwargs):
        deal_id = kwargs["deal_id"]
        try:
            if '_' in deal_id:
                deal = deal_from_activity_id_and_timestamp(deal_id)
            else:
                deal = Deal(deal_id)
        except ObjectDoesNotExist:
            return HttpResponse('Deal %s does not exist' % deal_id, status=404)
        return self.render_forms(request, self.get_context(deal, kwargs))

    def get_context(self, deal, kwargs):
        context = super().get_context_data(**kwargs)
        context['deal'] = {
            'id': deal.activity.id,
            'activity_identifier': deal.activity.activity_identifier,
            'attributes': deal.attributes,
            'primary_investor': deal.operational_stakeholder,
            'stakeholder': deal.stakeholders,
        }
        context['forms'] = get_forms(deal)
        context['investor'] = deal.stakeholders
        try:
            context['history'] = DealHistoryItem.get_history_for(deal)
        except AttributeError:
            pass
        return context

    def render_forms(self, request, context):
        return render_to_response(self.template_name, context, RequestContext(request))

    def render_forms_to_string(self, request, context):
        return render_to_string(self.template_name, context, RequestContext(request))


def display_valid_forms(forms):
    activity_identifier = Activity.objects.values().aggregate(Max('activity_identifier'))[
                              'activity_identifier__max'] + 1
    activity = Activity(activity_identifier=activity_identifier, fk_status_id=1, version=1)
    for form in forms:
        if name_of_form(form) == 'investor_info':
            print('investor_info', form.cleaned_data)
        elif name_of_form(form) == 'data_sources':
            for sub_form_data in form.cleaned_data:
                if sub_form_data['type'] and isinstance(sub_form_data['type'], int):
                    field = DealDataSourceForm().fields['type']
                    choices = dict(field.choices)
                    sub_form_data['type'] = str(choices[sub_form_data['type']])
                group = create_attribute_group(activity, sub_form_data)
                print(name_of_form(form), group)
        elif name_of_form(form) == 'spatial_data':
            for sub_form_data in form.cleaned_data:
                if sub_form_data['target_country'] and isinstance(sub_form_data['target_country'], Country):
                    sub_form_data['target_country'] = sub_form_data['target_country'].pk
                group = create_attribute_group(activity, sub_form_data)
                print(name_of_form(form), group)
        else:
            if any(form.cleaned_data.values()):
                group = create_attribute_group(activity, form.cleaned_data)
                print(name_of_form(form), group)
            else:
                print('no data sent:', name_of_form(form))


def display_invalid_forms(forms):
    for form in forms:
        if form.is_valid():
            print(form.__class__.__name__, form.cleaned_data)
        else:
            print(form.__class__.__name__, 'INVALID:', form.errors)


def get_forms(deal):
    forms = [get_form(deal, form) for form in FORMS]
    return forms


def get_form(deal, form_class):
    data = form_class[1].get_data(deal)
    return form_class[1](initial=data)


def deal_from_activity_id_and_timestamp(id_and_timestamp):
    from datetime import datetime
    from dateutil.tz import tzlocal
    if '_' in id_and_timestamp:
        activity_identifier, timestamp = id_and_timestamp.split('_')

        activity = Activity.objects.filter(activity_identifier=activity_identifier).order_by('id').last()
        if activity is None:
            raise ObjectDoesNotExist('activity_identifier %s' % activity_identifier)

        history = activity.history.filter(history_date__lte=datetime.fromtimestamp(float(timestamp), tz=tzlocal())).\
            filter(fk_status_id__in=(2, 3)).last()
        if history is None:
            raise ObjectDoesNotExist('Public deal with activity_identifier %s as of timestamp %s' % (activity_identifier, timestamp))

        return DealHistoryItem.from_activity_with_date(history, datetime.fromtimestamp(float(timestamp), tz=tzlocal()))

    raise RuntimeError('should contain _ separating activity id and timestamp: ' + id_and_timestamp)
