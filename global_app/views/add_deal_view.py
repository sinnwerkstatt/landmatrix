
from global_app.forms.add_deal_employment_form import AddDealEmploymentForm
from global_app.forms.add_deal_general_form import AddDealGeneralForm
from global_app.forms.add_deal_overall_comment_form import AddDealOverallCommentForm
from global_app.forms.change_deal_action_comment_form import ChangeDealActionCommentForm
from global_app.forms.deal_data_source_form import AddDealDataSourceFormSet, DealDataSourceForm
from global_app.forms.deal_former_use_form import DealFormerUseForm
from global_app.forms.deal_gender_related_info_form import DealGenderRelatedInfoForm
from global_app.forms.deal_local_communities_form import DealLocalCommunitiesForm
from global_app.forms.deal_produce_info_form import DealProduceInfoForm
from global_app.forms.deal_secondary_investor_formset import DealSecondaryInvestorFormSet, get_investors
from global_app.forms.deal_spatial_form import AddDealSpatialFormSet
from global_app.forms.deal_water_form import DealWaterForm
from landmatrix.models.activity import Activity
from landmatrix.models.activity_attribute_group import ActivityAttributeGroup
from landmatrix.models.country import Country
from .view_aux_functions import render_to_response

from django.views.generic import TemplateView
from django.template import RequestContext
from django.db.models import Max
from datetime import date

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

FORMS = [
    ("spatial_data", AddDealSpatialFormSet),            #
    ("general_information", AddDealGeneralForm),        #
    ("employment", AddDealEmploymentForm),              #
    ("investor_info", DealSecondaryInvestorFormSet),
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
                print(activity_identifier)
                activity = Activity(activity_identifier=activity_identifier, fk_status_id=1, version=1)

                for form in forms:
                    if name_of_form(form) == 'investor_info':
                        print('investor_info', form.cleaned_data)
                    elif name_of_form(form) == 'data_sources':
                        for sub_form_data in form.cleaned_data:
                            group = ActivityAttributeGroup(fk_activity=activity, date=date.today())
                            if sub_form_data['type'] and isinstance(sub_form_data['type'], int):
                                field = DealDataSourceForm().fields['type']
                                choices = dict(field.choices)
                                sub_form_data['type'] = str(choices[sub_form_data['type']])
                            group.attributes = { key: value for key, value in sub_form_data.items() if value }
                            print(name_of_form(form), group)
                    elif name_of_form(form) == 'spatial_data':
                        for sub_form_data in form.cleaned_data:
                            group = ActivityAttributeGroup(fk_activity=activity, date=date.today())
                            if sub_form_data['target_country'] and isinstance(sub_form_data['target_country'], Country):
                                sub_form_data['target_country'] = sub_form_data['target_country'].pk
                            group.attributes = { key: value for key, value in sub_form_data.items() if value }
                            #print(name_of_form(form), group)
                    else:
                        if any(form.cleaned_data.values()):
                            group = ActivityAttributeGroup(fk_activity=activity, date=date.today())
                            group.attributes = { key: value for key, value in form.cleaned_data.items() if value }
                            #print(name_of_form(form), group)
                        else:
                            print('no data sent:', name_of_form(form))

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