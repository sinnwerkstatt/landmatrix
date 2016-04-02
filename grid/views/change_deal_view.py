from pprint import pprint

from django.forms.formsets import BaseFormSet

from grid.forms.change_deal_general_form import ChangeDealGeneralForm
from .save_deal_view import SaveDealView
from landmatrix.models.activity import Activity
from landmatrix.models.deal import Deal

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


class ChangeDealView(SaveDealView):

    FORMS = [
        ("spatial_data", ChangeDealSpatialFormSet),
        ("general_information", ChangeDealGeneralForm),
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

    template_name = 'change-deal.html'

    def dispatch(self, request, *args, **kwargs):
        if 'deal_id' in kwargs:
            self.activity = Activity.objects.get(activity_identifier=kwargs.get('deal_id'))
        return super(ChangeDealView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**self.kwargs)
        context['deal_id'] = kwargs.pop('deal_id')
        return context

    def get_forms(self, data=None):
        return [self.get_form(form, data) for form in self.FORMS]

    def get_form(self, form_class, data=None):
        deal = Deal(self.activity.activity_identifier)
        initial = form_class[1].get_data(deal)
        #if issubclass(form_class[1], BaseFormSet):
        #    data = to_formset_data(data)
        return form_class[1](initial=initial, data=data)


def to_formset_data(data):
    returned = {}
    for index in data.keys():
        if not isinstance(index, int):
            returned[index] = data[index]
        else:
            for key, value in data[index].items():
                returned['form-{}-{}'.format(index, key)] = value
    return returned

