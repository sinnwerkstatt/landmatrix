from pprint import pprint

from django.forms.formsets import BaseFormSet

from grid.forms.change_deal_general_form import ChangeDealGeneralForm
from grid.forms.deal_contract_form import DealContractFormSet
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
from grid.forms.deal_spatial_form import DealSpatialFormSet
from grid.forms.deal_water_form import DealWaterForm
from grid.forms.deal_vggt_form import DealVGGTForm
from grid.forms.operational_stakeholder_form import OperationalStakeholderForm
from grid.forms.country_specific_forms import get_country_specific_form_classes


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class ChangeDealView(SaveDealView):

    FORMS = [
        DealSpatialFormSet,
        ChangeDealGeneralForm,
        DealContractFormSet,
        AddDealEmploymentForm,
        OperationalStakeholderForm,
        AddDealDataSourceFormSet,
        DealLocalCommunitiesForm,
        DealFormerUseForm,
        DealProduceInfoForm,
        DealWaterForm,
        DealGenderRelatedInfoForm,
        DealVGGTForm,
        AddDealOverallCommentForm,
        ChangeDealActionCommentForm,
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

    def get_forms(self, data=None, files=None):
        deal = Deal(self.activity.activity_identifier)
        forms = []

        for form_class in self.FORMS:
            form = self.get_form(deal, form_class, data=data, files=files)
            forms.append(form)

        for form_class in get_country_specific_form_classes(self.activity):
            country_specific_form = self.get_form(deal, form_class,
                                                  data=data, files=files)
            forms.append(country_specific_form)

        return forms

    def get_form(self, deal, form_class, **kwargs):
        kwargs['initial'] = form_class.get_data(deal)
        if 'prefix' not in kwargs:
            kwargs['prefix'] = self.get_form_prefix(form_class)
        form = form_class(**kwargs)

        return form


def to_formset_data(data):
    returned = {}
    for index in data.keys():
        if not isinstance(index, int):
            returned[index] = data[index]
        else:
            for key, value in data[index].items():
                returned['form-{}-{}'.format(index, key)] = value
    return returned
