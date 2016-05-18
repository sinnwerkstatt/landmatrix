from grid.forms.add_deal_employment_form import AddDealEmploymentForm
from grid.forms.add_deal_general_form import AddDealGeneralForm
from grid.forms.add_deal_overall_comment_form import AddDealOverallCommentForm
from grid.forms.change_deal_action_comment_form import ChangeDealActionCommentForm
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

from landmatrix.models.activity_attribute_group import ActivityAttributeGroup
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
        AddDealGeneralForm,
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
    deal_id = None
    activity = None
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

    def get_form_prefix(self, form_class):
        if form_class == DealSpatialFormSet:
            prefix = 'location'
        # TODO: rename AddDealDataSourceFormSet, it is used for both add and
        # change
        elif form_class == AddDealDataSourceFormSet:
            prefix = 'data_source'
        elif form_class == DealContractFormSet:
            prefix = 'contract'
        else:
            prefix = None

        return prefix

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        forms = self.get_forms(self.request.POST, files=self.request.FILES)
        if all(form.is_valid() for form in forms):
            action_comment = self.update_deal(forms, request)
            self.activity.fk_status = Status.objects.get(name='pending')
            self.activity.save()
            self.write_changeset(action_comment)
        else:
            messages.error(request, _('Please correct the error below.'))
        context['forms'] = forms
        return self.render_to_response(context)

    def write_changeset(self, action_comment):
        changeset = ActivityChangeset(fk_activity=self.activity, comment=action_comment, timestamp=datetime.now())
        changeset.save()

    def update_deal(self, forms, request):
        action_comment = ''
        # Delete existing attribute groups
        # FIXME: Why?
        ActivityAttributeGroup.objects.filter(fk_activity=self.activity).delete()
        # Create new attribute groups
        for form in forms:
            attributes = form.get_attributes(request)
            if not attributes:
                continue
            # Formset?
            if isinstance(attributes, list):
                for count, form_attributes in enumerate(attributes):
                    if form_attributes:
                        ActivityAttributeGroup.objects.create(
                            fk_activity=self.activity,
                            date=date.today(),
                            name='%s_%i' % (form.Meta.name, count),
                            attributes=form_attributes,
                            fk_language=Language.objects.get(english_name='English')
                        )
            # Form
            elif attributes:
                ActivityAttributeGroup.objects.create(
                    fk_activity=self.activity,
                    date=date.today(),
                    name=form.Meta.name,
                    attributes=attributes,
                    fk_language=Language.objects.get(english_name='English')
                )
            # Investor form?
            if form.Meta.name == 'investor_info' and form.cleaned_data['operational_stakeholder']:
                self.update_investor(form, request)

            if form.Meta.name == 'action_comment':
                action_comment = form.cleaned_data['tg_action_comment']

        return action_comment

    def update_investor(self, form, request):
        operational_stakeholder = form.cleaned_data['operational_stakeholder']
        # Update operational stakeholder (involvement)
        involvements = InvestorActivityInvolvement.objects.filter(fk_activity=self.activity)
        if len(involvements) > 1:
            raise MultipleObjectsReturned(
                'More than one operational stakeholder for activity {}'.format(str(self.activity))
            )
        if len(involvements):
            involvement = involvements.last()
            involvement.fk_investor = operational_stakeholder
        else:
            involvement = InvestorActivityInvolvement(
                fk_activity=self.activity, fk_investor=operational_stakeholder, fk_status_id=1
            )
        involvement.save()
        messages.success(request, self.success_message.format(self.deal_id))

