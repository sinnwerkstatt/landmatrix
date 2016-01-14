from global_app.forms.change_deal_employment_form import ChangeDealEmploymentForm
from global_app.forms.change_deal_general_form import ChangeDealGeneralForm
from global_app.forms.deal_data_source_form import PublicViewDealDataSourceFormSet, DealDataSourceForm
from global_app.forms.deal_former_use_form import DealFormerUseForm
from global_app.forms.deal_gender_related_info_form import DealGenderRelatedInfoForm
from global_app.forms.deal_local_communities_form import DealLocalCommunitiesForm
from global_app.forms.deal_produce_info_form import PublicViewDealProduceInfoForm
from global_app.forms.deal_spatial_form import PublicViewDealSpatialForm
from global_app.forms.deal_water_form import DealWaterForm
from global_app.forms.operational_stakeholder_form import OperationalStakeholderForm
from global_app.views.add_deal_view import name_of_form, create_attribute_group
from global_app.views.view_aux_functions import render_to_string, render_to_response

from landmatrix.models import Deal
from landmatrix.models.activity import Activity

from landmatrix.models.country import Country

from django.db.models import Max

from django.views.generic import TemplateView
from django.template import RequestContext

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

    def wrong_dispatch(self, request, *args, **kwargs):
        forms = get_forms(request.POST)

        # check whether it's valid:
        if all(form.is_valid() for form in forms):

            activity_identifier = Activity.objects.values().aggregate(Max('activity_identifier'))['activity_identifier__max']+1
            activity = Activity(activity_identifier=activity_identifier, fk_status_id=1, version=1)

            print('all valid:', forms)
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

                print(form)

        else:
            print('NOT all valid:', forms)
            for form in forms:
                if form.is_valid():
                    print(form.__class__.__name__, form.cleaned_data)
                else:
                    print(form.__class__.__name__, 'INVALID:', form.errors)

        # if a GET (or any other method) we'll create a blank form

        context = super().get_context_data(**kwargs)
        context['forms'] = forms
        return render_to_response(self.template_name, context, RequestContext(request))

    def dispatch(self, request, *args, **kwargs):
        deal = Deal(kwargs["deal_id"])
        context = self.get_context(deal, kwargs)
        context['history'] = [
            history_item for history_item in deal.get_history()
            ]

        return self.render_forms(request, context)

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
        # context['investor'] = get_investors(deal)
        context['investor'] = deal.stakeholders
        return context

    def render_forms(self, request, context):
        return render_to_response(self.template_name, context, RequestContext(request))

    def render_forms_to_string(self, request, context):
        return render_to_string(self.template_name, context, RequestContext(request))


def get_forms(deal):
    forms = [get_form(deal, form) for form in FORMS]
    print('get forms:', forms)
    return forms


def get_form(deal, form_class):
    data = form_class[1].get_data(deal)
    return form_class[1](initial=data)
