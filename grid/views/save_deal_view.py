from grid.forms.add_deal_employment_form import AddDealEmploymentForm
from grid.forms.add_deal_general_form import AddDealGeneralForm
from grid.forms.add_deal_overall_comment_form import AddDealOverallCommentForm
from grid.forms.change_deal_action_comment_form import ChangeDealActionCommentForm
from grid.forms.deal_data_source_form import AddDealDataSourceFormSet, DealDataSourceForm
from grid.forms.deal_former_use_form import DealFormerUseForm
from grid.forms.deal_gender_related_info_form import DealGenderRelatedInfoForm
from grid.forms.deal_local_communities_form import DealLocalCommunitiesForm
from grid.forms.deal_produce_info_form import DealProduceInfoForm
from grid.forms.deal_spatial_form import AddDealSpatialFormSet
from grid.forms.deal_water_form import DealWaterForm
from grid.forms.investor_formset import InvestorFormSet
from grid.forms.operational_stakeholder_form import OperationalStakeholderForm

from landmatrix.models.activity_attribute_group import ActivityAttributeGroup
from landmatrix.models.country import Country
from landmatrix.models.investor import InvestorActivityInvolvement, Investor
from landmatrix.models.language import Language
from .view_aux_functions import render_to_response

from django.views.generic import TemplateView
from django.template import RequestContext

from django.db.models.query import QuerySet
from django.http.response import HttpResponseRedirect
from django.db import transaction
from django.db.models import Model

from datetime import date

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

FORMS = [
    ("spatial_data", AddDealSpatialFormSet),            #
    ("general_information", AddDealGeneralForm),        #
    ("employment", AddDealEmploymentForm),              #
    # ("investor_info", InvestorFormSet),
    ("investor_info", OperationalStakeholderForm),
    ("data_sources", AddDealDataSourceFormSet),         #
    ("local_communities", DealLocalCommunitiesForm),    #
    ("former_use", DealFormerUseForm),                  #
    ("produce_info", DealProduceInfoForm),              #
    ("water", DealWaterForm),                           #
    ("gender-related_info", DealGenderRelatedInfoForm), #
    ("overall_comment", AddDealOverallCommentForm),     #
    ("action_comment", ChangeDealActionCommentForm),
]


class SaveDealView(TemplateView):

    def dispatch(self, request, *args, **kwargs):
        self.activity = self.get_activity(**kwargs)

        forms = self.get_forms(request.POST)

        # if this is a POST request we need to process the form data
        if request.method == 'POST':

            # check whether it's valid:
            if all(form.is_valid() for form in forms):


                groups = []
                for form in forms:
                    groups.extend(self.create_attributes_for_form(self.activity, form))

                self.save_activity_and_attributes(self.activity, groups)

                # redirect to dashboard
                return HttpResponseRedirect('/dashboard/')

            else:
                for form in forms:
                    if form.is_valid():
                        print(form.__class__.__name__, form.cleaned_data)
                    else:
                        print(form.__class__.__name__, 'INVALID:', form.errors)

        # if a GET (or any other method) we'll create a blank form

        context = super().get_context_data(**kwargs)
        context['forms'] = forms
        context['kwargs'] = kwargs
        context['deal_id'] = kwargs.get('deal_id')
        print('context:', context)
        return render_to_response(self.template_name, context, RequestContext(request))

    @transaction.atomic
    def save_activity_and_attributes(self, activity, groups):
        activity.save()
        for group in groups:
            group.fk_activity = activity
            group.save()
        InvestorActivityInvolvement(
            fk_activity=activity, fk_investor_id=self.operational_stakeholder, fk_status_id=1
        ).save()

    def create_attributes_for_form(self,activity, form):
        groups = []

        if name_of_form(form) == 'investor_info':
            self.operational_stakeholder = form.cleaned_data['operational_stakeholder']

        elif name_of_form(form) == 'data_sources':
            for sub_form_data in form.cleaned_data:
                if sub_form_data['type'] and isinstance(sub_form_data['type'], int):
                    field = DealDataSourceForm().fields['type']
                    choices = dict(field.choices)
                    sub_form_data['type'] = str(choices[sub_form_data['type']])
                group = create_attribute_group(activity, sub_form_data)
                groups.append(group)

        elif name_of_form(form) == 'spatial_data':
            for sub_form_data in form.cleaned_data:
                if sub_form_data['target_country'] and isinstance(sub_form_data['target_country'], Country):
                    sub_form_data['target_country'] = sub_form_data['target_country'].pk
                group = create_attribute_group(activity, sub_form_data)
                groups.append(group)

        else:
            if any(form.cleaned_data.values()):
                group = create_attribute_group(activity, form.cleaned_data)
                groups.append(group)

            else:
                print('no data sent:', name_of_form(form))

        return groups



def create_attribute_group(activity, form_data):
    group = ActivityAttributeGroup(
        fk_activity=activity, date=date.today(),
        attributes = {key: model_to_id(value) for key, value in form_data.items() if value},
        fk_language=Language.objects.get(english_name='English')
    )
    return group


def name_of_form(form):
    for name, Form in FORMS:
        if Form == form.__class__:
            return name
    raise ValueError('Form %s not in FORMS' % form.__class__.__name__)


def model_to_id(value):
    if isinstance(value, QuerySet):
        return model_to_id(list(value))
    elif isinstance(value, Model):
        return value.pk
    elif isinstance(value, list):
        return [model_to_id(v) for v in value]
    else:
        return value

