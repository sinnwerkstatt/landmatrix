from django.db.models.query import QuerySet

from global_app.forms.add_deal_employment_form import AddDealEmploymentForm
from global_app.forms.add_deal_general_form import AddDealGeneralForm
from global_app.forms.add_deal_overall_comment_form import AddDealOverallCommentForm
from global_app.forms.change_deal_action_comment_form import ChangeDealActionCommentForm
from global_app.forms.deal_data_source_form import AddDealDataSourceFormSet, DealDataSourceForm
from global_app.forms.deal_former_use_form import DealFormerUseForm
from global_app.forms.deal_gender_related_info_form import DealGenderRelatedInfoForm
from global_app.forms.deal_local_communities_form import DealLocalCommunitiesForm
from global_app.forms.deal_produce_info_form import DealProduceInfoForm
from global_app.forms.deal_spatial_form import AddDealSpatialFormSet
from global_app.forms.deal_water_form import DealWaterForm
from global_app.forms.operational_stakeholder_form import OperationalStakeholderForm

from landmatrix.models.activity import Activity
from landmatrix.models.activity_attribute_group import ActivityAttributeGroup
from landmatrix.models.country import Country
from landmatrix.models.language import Language
from .view_aux_functions import render_to_response

from django.views.generic import TemplateView
from django.template import RequestContext
from django.db.models import Max, Model
from django.db import transaction
from datetime import date

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

FORMS = [
    ("spatial_data", AddDealSpatialFormSet),            #
    ("general_information", AddDealGeneralForm),        #
    ("employment", AddDealEmploymentForm),              #
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


class AddDealView(TemplateView):

    template_name = 'add-deal.html'

    def dispatch(self, request, *args, **kwargs):
        forms = get_forms(request.POST)

        # if this is a POST request we need to process the form data
        if request.method == 'POST':

            # check whether it's valid:
            if all(form.is_valid() for form in forms):

                activity_identifier = Activity.objects.values().aggregate(Max('activity_identifier'))['activity_identifier__max']+1
                activity = Activity(activity_identifier=activity_identifier, fk_status_id=1)

                groups = []
                for form in forms:
                    groups.extend(create_attributes_for_form(activity, form))

                self.save_activity_and_attributes(activity, groups)

                # redirect to a new URL:
                # return HttpResponseRedirect('/thanks/')

            else:
                for form in forms:
                    if form.is_valid():
                        print(form.__class__.__name__, form.cleaned_data)
                    else:
                        print(form.__class__.__name__, 'INVALID:', form.errors)

        # if a GET (or any other method) we'll create a blank form

        context = super().get_context_data(**kwargs)
        context['forms'] = forms
        return render_to_response(self.template_name, context, RequestContext(request))

    @transaction.atomic
    def save_activity_and_attributes(self, activity, groups):
        activity.save()
        # print('activity:', activity)
        # print('groups:', groups)
        for group in groups:
            group.fk_activity = activity
            # print('attributes:', group)
            group.save()

def create_attributes_for_form(activity, form):
    groups = []

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
            groups.append(group)

    elif name_of_form(form) == 'spatial_data':
        for sub_form_data in form.cleaned_data:
            if sub_form_data['target_country'] and isinstance(sub_form_data['target_country'], Country):
                sub_form_data['target_country'] = sub_form_data['target_country'].pk
            group = create_attribute_group(activity, sub_form_data)
            print(name_of_form(form), group)
            groups.append(group)

    else:
        if any(form.cleaned_data.values()):
            group = create_attribute_group(activity, form.cleaned_data)
            print(name_of_form(form), group)
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


def get_forms(data=None):
        forms = []
        for name, Form in FORMS:
            new_form = Form() if not data else Form(data)
            forms.append(new_form)
        return forms


def name_of_form(form):
    for name, Form in FORMS:
        if Form == form.__class__:
            return name
    raise ValueError('Form %s not in FORMS' % form.__class__.__name__)


def model_to_id(value):
    print('model to id:', value, type(value))
    if isinstance(value, QuerySet):
        return model_to_id(list(value))
    elif isinstance(value, Model):
        return value.pk
    elif isinstance(value, list):
        print('model to id is list:', value)
        return [model_to_id(v) for v in value]
    else:
        return value