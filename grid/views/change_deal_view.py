from pprint import pprint

from django.forms.formsets import BaseFormSet
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseRedirect

from grid.forms.deal_general_form import DealGeneralForm
from grid.forms.deal_contract_form import DealContractFormSet
from .save_deal_view import SaveDealView
from landmatrix.models.activity import Activity, HistoricalActivity
from landmatrix.models.deal_history import DealHistoryItem

from grid.forms.deal_employment_form import DealEmploymentForm
from grid.forms.deal_overall_comment_form import DealOverallCommentForm
from grid.forms.deal_action_comment_form import DealActionCommentForm
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
from grid.forms.public_user_information_form import PublicUserInformationForm


class ChangeDealView(SaveDealView):

    FORMS = [
        DealSpatialFormSet,
        DealGeneralForm,
        DealContractFormSet,
        DealEmploymentForm,
        OperationalStakeholderForm,
        AddDealDataSourceFormSet,
        DealLocalCommunitiesForm,
        DealFormerUseForm,
        DealProduceInfoForm,
        DealWaterForm,
        DealGenderRelatedInfoForm,
        DealVGGTForm,
        DealOverallCommentForm,
        DealActionCommentForm,
    ]

    template_name = 'change-deal.html'

    def dispatch(self, request, *args, **kwargs):
        return super(ChangeDealView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, deal_id, history_id=None):
        context = super().get_context_data(**self.kwargs)
        context.update({
            'deal_id': deal_id,
            'history_id': history_id,
            'activity': self.get_object(),
        })
        return context

    def get_object(self):
        # TODO: Cache result for user
        deal_id = self.kwargs.get('deal_id')
        history_id = self.kwargs.get('history_id', None)
        queryset = HistoricalActivity.objects
        if not self.request.user.has_perm('landmatrix.review_activity'):
            queryset = queryset.public(self.request.user)
        try:
            if history_id:
                activity = queryset.get(id=history_id)
            else:
                activity = queryset.filter(activity_identifier=deal_id).latest()
        except ObjectDoesNotExist as e:
            raise Http404('Activity %s does not exist (%s)' % (deal_id, str(e))) 
        if not self.request.user.has_perm('landmatrix.change_activity'):
            if activity.fk_status_id == activity.STATUS_DELETED:
                raise Http404('Activity %s has been deleted' % deal_id)
        return activity 

    def get_forms(self, data=None, files=None):
        forms = []
        for form_class in self.FORMS:
            # Add register form instead of action comment form for non authenticated user
            if form_class == DealActionCommentForm and not self.request.user.is_authenticated():
                forms.append(PublicUserInformationForm(data=data))
            else:
                forms.append(self.get_form(form_class, data=data, files=files))
        # Add country specific forms
        for form_class in get_country_specific_form_classes(self.get_object()):
            forms.append(self.get_form(form_class, data=data, files=files))
        return forms

    def get_form(self, form_class, data=None, files=None):
        prefix = issubclass(form_class, BaseFormSet) and form_class.Meta.name or None
        initial = form_class.get_data(self.get_object())
        return form_class(initial=initial, files=files, data=data, prefix=prefix)

    #def render_to_response(self, *args, **kwargs):
    #    '''
    #    If we have a shapefile upload, just reload the page so it displays
    #    correctly
    #    '''
    #    # TODO: remove this hack, make the different area fields handle this
    #    if any(['_area' in key for key in self.request.FILES.keys()]):
    #        return HttpResponseRedirect(
    #            self.request.META.get('HTTP_REFERER', '/'))
    #    return super().render_to_response(*args, **kwargs)


#def to_formset_data(data):
#    returned = {}
#    for index in data.keys():
#        if not isinstance(index, int):
#            returned[index] = data[index]
#        else:
#            for key, value in data[index].items():
#                returned['form-{}-{}'.format(index, key)] = value
#    return returned
