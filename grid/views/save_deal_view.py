from django.views.generic import TemplateView
from django.db import transaction
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden

from landmatrix.models.activity_attribute_group import (
    HistoricalActivityAttribute, ActivityAttributeGroup,
)
from landmatrix.models.activity import HistoricalActivity
from landmatrix.models.investor import (HistoricalInvestor, InvestorActivityInvolvement,
                                        HistoricalInvestorActivityInvolvement)
from landmatrix.models.activity_changeset import ActivityChangeset
from landmatrix.models.activity_feedback import ActivityFeedback
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
from grid.utils import has_perm_approve_reject


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
    success_message_admin = _('Your changes to the deal have been saved successfully.')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

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
        forms = self.get_forms(
            data=self.request.POST, files=self.request.FILES)
        if all(form.is_valid() for form in forms):
            return self.form_valid(forms)
        else:
            return self.form_invalid(forms)

    def form_valid(self, forms):
        old_hactivity = self.get_object()
        investor_form = list(filter(lambda f: isinstance(f, OperationalStakeholderForm), forms))[0]
        is_admin = self.request.user.has_perm('landmatrix.change_activity')
        is_editor = self.request.user.has_perm('landmatrix.review_activity')

        if old_hactivity.fk_status_id == HistoricalActivity.STATUS_PENDING:
            # Only editors and administrators are allowed to edit pending versions
            if not is_editor and not is_admin:
                raise HttpResponseForbidden('Deal version is pending')

        # Create new historical activity
        hactivity = HistoricalActivity(
            activity_identifier=old_hactivity.activity_identifier,
            fk_status_id=HistoricalActivity.STATUS_PENDING,
            history_user=self.request.user)
        hactivity.save(update_elasticsearch=False)

        # Create new activity attributes
        hactivity.comment = self.create_attributes(hactivity, forms)
        form = self.get_form_by_type(forms, DealActionCommentForm)
        if form:
            hactivity.fully_updated = self.get_fully_updated(form)
        else:
            hactivity.fully_updated = False
        hactivity.save(update_elasticsearch=False)
        self.create_involvement(hactivity, investor_form)

        # Create activity feedback
        form = self.get_form_by_type(forms, DealActionCommentForm)
        if form:
            self.create_activity_feedback(hactivity, form)

        if not is_admin:
            self.create_activity_changeset(hactivity)

        if 'approve_btn' in self.request.POST and has_perm_approve_reject(self.request.user, hactivity):
            messages.success(self.request, self.success_message_admin.format(hactivity.activity_identifier))
            hactivity.approve_change(self.request.user, '')
        elif 'reject_btn' in self.request.POST and has_perm_approve_reject(self.request.user, hactivity):
            hactivity.reject_change(self.request.user, '')
        else:
            messages.success(self.request, self.success_message.format(hactivity.activity_identifier))

        return redirect('deal_detail', deal_id=hactivity.activity_identifier)

    def form_invalid(self, forms):
        messages.error(self.request, _('Please correct the error below.'))

        context = self.get_context_data(**self.kwargs)
        context['forms'] = forms
        return self.render_to_response(context)

    def create_attributes(self, activity, forms):
        action_comment = ''
        # Create new attributes
        for form in forms:
            if form.Meta.name in ('action_comment', 'user_information'):
                action_comment = form.cleaned_data['tg_action_comment']

            attributes = form.get_attributes(request=self.request)
            if not attributes:
                continue
            # Formset?
            if isinstance(attributes, list):
                # Loop forms
                for count, form_attributes in enumerate(attributes):
                    if form_attributes:
                        aag, created = ActivityAttributeGroup.objects.get_or_create(
                            name='%s_%02i' % (form.Meta.name, count + 1), # two digits required for ordering
                        )
                        # Loop fields
                        for name, attribute in form_attributes.items():
                            if isinstance(attribute, dict):
                                attribute = [attribute]
                            # Loop values (= attributes)
                            for kwargs in attribute:
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
                # Loop fields
                for name, attribute in attributes.items():
                    if not isinstance(attribute, (list, tuple)):
                        attribute = [attribute]
                    # Loop values (= attributes)
                    for kwargs in attribute:
                        kwargs.update({
                            'name': name,
                            'fk_activity': activity,
                            'fk_group': aag,
                            'fk_language_id': 1,
                        })
                        aa = HistoricalActivityAttribute.objects.create(**kwargs)

        return action_comment

    def create_involvement(self, hactivity, form):
        hinvestor = form.cleaned_data['operational_stakeholder']
        # Operating company given?
        if hinvestor:
            hinvolvement = HistoricalInvestorActivityInvolvement.objects.create(
                fk_activity=hactivity,
                fk_investor=hinvestor,
                fk_status_id=hactivity.STATUS_PENDING,
            )

    def get_form_by_type(self, forms, type):
        form = list(filter(lambda f: isinstance(f, type), forms))
        if len(form) == 0:
            return
        else:
            return form[0]       

    def create_activity_feedback(self, activity, form):
        data = form.cleaned_data
        if data.get('assign_to_user', None):
            ActivityFeedback.objects.filter(fk_activity__activity_identifier=self.get_object().activity_identifier).delete()
            feedback = ActivityFeedback.objects.create(
                fk_activity_id=self.get_object().id,
                fk_user_assigned=data.get('assign_to_user'),
                fk_user_created=self.request.user,
                comment=data.get('tg_feedback_comment'),
            )

    def get_fully_updated(self, form):
        return form.cleaned_data.get('fully_updated', False)

    def create_activity_changeset(self, activity):
        # Create changeset (for review)
        country = activity.target_country
        try:
            user = self.request.user.userregionalinfo.super_user
        except (AttributeError, ObjectDoesNotExist):
            user = None
        changeset = ActivityChangeset.objects.create(
            fk_activity=activity,
            fk_country=country,
            #fk_region=country and country.region
            fk_user=user,
        )
        return changeset
