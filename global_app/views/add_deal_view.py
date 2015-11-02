from collections import OrderedDict
from global_app.forms.add_deal_employment_form import AddDealEmploymentForm
from global_app.forms.add_deal_general_form import AddDealGeneralForm
from global_app.forms.add_deal_overall_comment_form import AddDealOverallCommentForm
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

FORMS = OrderedDict([
    ("spatial_data", AddDealSpatialFormSet),
    ("general_information", AddDealGeneralForm),
    ("employment", AddDealEmploymentForm),
    ("investor_info", DealSecondaryInvestorFormSet),
    ("data_sources", AddDealDataSourceFormSet),
    ("local_communities", DealLocalCommunitiesForm),
    ("former_use", DealFormerUseForm),
    ("produce_info", DealProduceInfoForm),
    ("water", DealWaterForm),
    ("gender-related_info", DealGenderRelatedInfoForm),
    ("overall_comment", AddDealOverallCommentForm),
    # ("action_comment", ChangeDealActionCommentForm),
    # ("history", DealHistoryForm)
])

class AddDealView(TemplateView):

    template_name = 'add-deal.html'

    def dispatch(self, request, *args, **kwargs):

        context = super().get_context_data(**kwargs)
        context['forms'] = get_forms()
#        context['investor'] = get_investors(deal)

        return render_to_response(self.template_name, context, RequestContext(request))


def get_forms():
        forms = []
        for name, Form in FORMS.items():
            new_form = Form()
            forms.append(new_form)
        return forms

