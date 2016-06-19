from grid.forms.deal_employment_form import DealEmploymentForm
from grid.forms.deal_general_form import DealGeneralForm
from grid.forms.deal_overall_comment_form import DealOverallCommentForm
from grid.forms.deal_action_comment_form import DealActionCommentForm
from grid.forms.deal_contract_form import DealContractFormSet
from grid.forms.deal_data_source_form import AddDealDataSourceFormSet
from grid.forms.deal_former_use_form import DealFormerUseForm
from grid.forms.deal_gender_related_info_form import DealGenderRelatedInfoForm
from grid.forms.deal_local_communities_form import DealLocalCommunitiesForm
from grid.forms.deal_produce_info_form import DealProduceInfoForm
from grid.forms.deal_spatial_form import DealSpatialFormSet
from grid.forms.deal_water_form import DealWaterForm
from grid.forms.deal_vggt_form import DealVGGTForm
from grid.forms.operational_stakeholder_form import OperationalStakeholderForm

from landmatrix.models.activity_attribute_group import ActivityAttribute, \
    HistoricalActivityAttribute, ActivityAttributeGroup
from landmatrix.models.activity import Activity
from landmatrix.models.activity_changeset import ActivityChangeset
from landmatrix.models.investor import InvestorActivityInvolvement
from landmatrix.models.language import Language
from landmatrix.models.status import Status

from django.views.generic import TemplateView

from django.db import transaction
from django.contrib import messages
from django.core.exceptions import MultipleObjectsReturned
from django.utils.translation import ugettext_lazy as _

from datetime import date, datetime

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class SaveDealView(TemplateView):
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
    deal_id = None
    success_message = _('Your changes to the deal have been submitted successfully. The changes will be reviewed and published soon.')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**self.kwargs)
        if self.request.method != 'POST':
            context['forms'] = self.get_forms()
        context['kwargs'] = self.kwargs
        return context

    def get_forms(self, data=None, files=None):
        raise NotImplementedError("get_forms must be implemented in "
                                  "subclasses.")

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        forms = self.get_forms(self.request.POST, files=self.request.FILES)
        if all(form.is_valid() for form in forms):
            activity = self.get_object()
            # Create new historical activity
            activity.pk = None
            if not request.user.is_superuser:
                activity.fk_status_id = 1
            activity.save()
            # Create new activity attributes
            action_comment = self.update_deal(activity, forms, request)
            # Create changeset
            changeset = ActivityChangeset.objects.create(
                fk_activity=activity,
                comment=action_comment
            )
            messages.success(request, self.success_message.format(self.deal_id))
        else:
            messages.error(request, _('Please correct the error below.'))
        context['forms'] = forms
        return self.render_to_response(context)

    def update_deal(self, activity, forms, request):
        action_comment = ''
        # Create new attributes
        for form in forms:
            attributes = form.get_attributes(request)
            if not attributes:
                continue
            # Formset?
            if isinstance(attributes, list):
                for count, form_attributes in enumerate(attributes):
                    if form_attributes:
                        aag, created = ActivityAttributeGroup.objects.get_or_create(
                            name='%s_%i' % (form.Meta.name, count),
                        )
                        for name, kwargs in form_attributes.items():
                            kwargs.update({
                                'name': name,
                                'fk_activity': activity,
                                'fk_group': aag,
                                'fk_language_id': 1,
                            })
                            aa = HistoricalActivityAttribute.objects.create(**kwargs)
            # Form
            elif attributes:
                aag, created = ActivityAttributeGroup.objects.get_or_create(
                    name=form.Meta.name
                )
                for name, kwargs in attributes.items():
                    kwargs.update({
                        'name': name,
                        'fk_activity': activity,
                        'fk_group': aag,
                        'fk_language_id': 1,
                    })
                    aa = HistoricalActivityAttribute.objects.create(**kwargs)
            # Investor form?
            if form.Meta.name == 'investor_info' and form.cleaned_data['operational_stakeholder']:
                self.update_investor(form, request)

            if form.Meta.name == 'action_comment':
                action_comment = form.cleaned_data['tg_action_comment']

        return action_comment

    def update_investor(self, form, request):
        # FIXME
        # Problem here: Involvements are not historical yet, but activity and investors are.
        # As an intermediate solution we'll just create another involvement which links
        # to the public activity, which will replace the current involvement when the
        # historical activity gets approved. 
        activity = Activity.objects.get(activity_identifier=self.kwargs.get('deal_id'))

        operational_stakeholder = form.cleaned_data['operational_stakeholder']
        # Update operational stakeholder (involvement)
        #involvements = InvestorActivityInvolvement.objects.filter(fk_activity=activity)
        #if len(involvements) > 1:
        #    raise MultipleObjectsReturned(
        #        'More than one operational stakeholder for activity %s' % str(self.get_object())
        #    )
        #elif len(involvements):
        #    involvement = involvements.last()
        #    involvement.fk_investor = operational_stakeholder
        #else:
        involvement = InvestorActivityInvolvement.objects.create(
            fk_activity=activity,
            fk_investor=operational_stakeholder,
            fk_status_id=1
        )
        involvement.save()

