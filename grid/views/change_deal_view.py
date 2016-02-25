from pprint import pprint

from django.forms.forms import Form

from landmatrix.models.activity import Activity
from landmatrix.models.deal import Deal
from .save_deal_view import SaveDealView

from grid.forms.add_deal_employment_form import AddDealEmploymentForm
from grid.forms.add_deal_general_form import AddDealGeneralForm
from grid.forms.add_deal_overall_comment_form import AddDealOverallCommentForm
from grid.forms.change_deal_action_comment_form import ChangeDealActionCommentForm
from grid.forms.deal_data_source_form import AddDealDataSourceFormSet
from grid.forms.deal_former_use_form import DealFormerUseForm
from grid.forms.deal_gender_related_info_form import DealGenderRelatedInfoForm
from grid.forms.deal_local_communities_form import DealLocalCommunitiesForm
from grid.forms.deal_produce_info_form import DealProduceInfoForm
from grid.forms.deal_spatial_form import ChangeDealSpatialFormSet
from grid.forms.deal_water_form import DealWaterForm
from grid.forms.operational_stakeholder_form import OperationalStakeholderForm

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

FORMS = [
    ("spatial_data", ChangeDealSpatialFormSet),
    ("general_information", AddDealGeneralForm),
    ("employment", AddDealEmploymentForm),
    ("investor_info", OperationalStakeholderForm),
    ("data_sources", AddDealDataSourceFormSet),
    ("local_communities", DealLocalCommunitiesForm),
    ("former_use", DealFormerUseForm),
    ("produce_info", DealProduceInfoForm),
    ("water", DealWaterForm),
    ("gender-related_info", DealGenderRelatedInfoForm),
    ("overall_comment", AddDealOverallCommentForm),
    ("action_comment", ChangeDealActionCommentForm),
]


class ChangeDealView(SaveDealView):

    template_name = 'change-deal.html'

    def get_activity(self, **kwargs):
        return Activity.objects.get(activity_identifier=kwargs.get('deal_id'))

    def get_forms(self, data=None):
        return [get_form(Deal(self.activity.activity_identifier), form) for form in FORMS]


def get_form(deal, form_class):
    data = form_class[1].get_data(deal)
    if form_class[0] == 'data_sources':
        print('get_form:', form_class[0], form_class[1].__name__)
        # pprint(data)
    return form_class[1](initial=data)
