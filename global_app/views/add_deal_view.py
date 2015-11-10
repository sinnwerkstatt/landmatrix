from collections import OrderedDict
from global_app.forms.add_deal_employment_form import AddDealEmploymentForm
from global_app.forms.add_deal_general_form import AddDealGeneralForm
from global_app.forms.add_deal_overall_comment_form import AddDealOverallCommentForm
from global_app.forms.change_deal_action_comment_form import ChangeDealActionCommentForm
from global_app.forms.deal_data_source_form import AddDealDataSourceFormSet
from global_app.forms.deal_former_use_form import DealFormerUseForm
from global_app.forms.deal_gender_related_info_form import DealGenderRelatedInfoForm
from global_app.forms.deal_local_communities_form import DealLocalCommunitiesForm
from global_app.forms.deal_produce_info_form import DealProduceInfoForm
from global_app.forms.deal_secondary_investor_formset import DealSecondaryInvestorFormSet, get_investors
from global_app.forms.deal_spatial_form import AddDealSpatialFormSet
from global_app.forms.deal_water_form import DealWaterForm

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from landmatrix.models import Deal
from .view_aux_functions import render_to_response

from django.views.generic import TemplateView
from django.template import RequestContext

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
            print('POST:', request.POST)
            # create a form instance and populate it with data from the request:

            # check whether it's valid:
            valid = [form.is_valid() for form in forms]
            if all(valid):
                for form in forms:
                    # process the data in form.cleaned_data as required
                    print('cleaned data:', form.cleaned_data)
                    # redirect to a new URL:
                    #return HttpResponseRedirect('/thanks/')
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

