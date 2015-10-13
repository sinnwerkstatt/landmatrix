from copy import copy
from global_app.forms.change_deal_action_comment_form import ChangeDealActionCommentForm
from global_app.forms.change_deal_employment_form import ChangeDealEmploymentForm
from global_app.forms.change_deal_general_form import ChangeDealGeneralForm
from global_app.forms.change_deal_overall_comment_form import ChangeDealOverallCommentForm
from global_app.forms.deal_data_source_form import ChangeDealDataSourceFormSet
from global_app.forms.deal_former_use_form import DealFormerUseForm
from global_app.forms.deal_gender_related_info_form import DealGenderRelatedInfoForm
from global_app.forms.deal_history_form import DealHistoryForm
from global_app.forms.deal_local_communities_form import DealLocalCommunitiesForm
from global_app.forms.deal_produce_info_form import PublicViewDealProduceInfoForm
from global_app.forms.deal_secondary_investor_formset import DealSecondaryInvestorFormSet
from global_app.forms.deal_spatial_form import PublicViewDealSpatialForm
from global_app.forms.deal_water_form import DealWaterForm

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from landmatrix.models import Deal
from .view_aux_functions import render_to_response

from django.views.generic import TemplateView
from django.template import RequestContext


FORMS = [
    ("spatial_data", PublicViewDealSpatialForm),
#    ("general_information", ChangeDealGeneralForm),
#     ("employment", ChangeDealEmploymentForm),
#!     ("investor_info", DealSecondaryInvestorFormSet),
#!     ("data_sources", ChangeDealDataSourceFormSet),
#     ("local_communities", DealLocalCommunitiesForm),
#     ("former_use", DealFormerUseForm),
#     ("produce_info", PublicViewDealProduceInfoForm),
#     ("water", DealWaterForm),
    ("gender-related_info", DealGenderRelatedInfoForm),
    # ("overall_comment", ChangeDealOverallCommentForm),
    # ("action_comment", ChangeDealActionCommentForm),
    # ("history", DealHistoryForm)
]

class DealDetailView(TemplateView):

    template_name = 'deal-detail.html'

    def dispatch(self, request, *args, **kwargs):

        deal = Deal(kwargs["deal_id"])
        context = super().get_context_data(**kwargs)
        context['deal'] = {
                'attributes': deal.attributes,
                'primary_investor': deal.primary_investor,
                'stakeholder': deal.stakeholder,
        }
        context['forms'] = self.get_forms(deal)

        return render_to_response(self.template_name, context, RequestContext(request))

    def get_forms(self, deal):
        forms = []
        for form in FORMS:
            data = form[1].get_data(deal)
            new_form = form[1](data=data)
            forms.append(new_form)
        return forms
