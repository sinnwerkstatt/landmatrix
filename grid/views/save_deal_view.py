from datetime import datetime

from django.views.generic import TemplateView
from django.db import transaction
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from django.conf import settings

from landmatrix.models.activity_attribute_group import (
    HistoricalActivityAttribute, ActivityAttributeGroup,
)
from landmatrix.models.activity import Activity
from landmatrix.models.investor import InvestorActivityInvolvement
from landmatrix.models.activity_changeset import ActivityChangeset
from landmatrix.models.activity_feedback import ActivityFeedback
from editor.models import UserRegionalInfo
from grid.forms.public_user_information_form import PublicUserInformationForm
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
    success_message_admin = _('Your changes to the deal have been saved successfully.')

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
        forms = self.get_forms(self.request.POST, files=self.request.FILES)
        if all(form.is_valid() for form in forms):
            # Register user if not authenticated
            if not self.request.user.is_authenticated():
                user_information_form = self.get_form_by_type(
                    forms, PublicUserInformationForm)
                user = self._get_or_create_user(user_information_form)
                self.login_user(user)
            return self.form_valid(forms)
        else:
            return self.form_invalid(forms)

    def _get_or_create_user(self, user_information_form):
        # TODO: this is really bad practice. Why not a form that makes it
        # clear to the user that they are creating an account?
        if not user_information_form:
            raise ValidationError(
                _('User is not authenticated and no user information given.'))
        data = user_information_form.cleaned_data
        try:
            user = User.objects.get(
                email=data['public_user_email'])
        except User.DoesNotExist:
            names = data['public_user_name'].split(' ')
            if len(names) > 1:
                first_name = ' '.join(names[:-1])
                last_name = names[-1]
            else:
                first_name = names[0]
                last_name = ''

            user = User.objects.create_user(
                data['public_user_email'],
                email=data['public_user_email'],
                password=None,
                first_name=first_name,
                last_name=last_name,
            )
            UserRegionalInfo.objects.create(
                user=user,
                phone=data['public_user_phone'],
            )
            group, created = Group.objects.get_or_create(name='Reporters')
            user.groups.add(group)

        return user

    def form_valid(self, forms):
        hactivity = self.get_object()
        investor_form = list(filter(lambda f: isinstance(f, OperationalStakeholderForm), forms))[0]
        # Create new historical activity
        hactivity.pk = None
        hactivity.history_user = self.request.user
        hactivity.history_date = datetime.now()
        if not self.request.user.has_perm('landmatrix.change_activity'):
            hactivity.fk_status_id = hactivity.STATUS_PENDING
        hactivity.save()
        # Create new activity attributes
        hactivity.comment = self.create_attributes(hactivity, forms)
        form = self.get_form_by_type(forms, DealActionCommentForm)
        if form:
            hactivity.fully_updated = self.get_fully_updated(form)
        else:
            hactivity.fully_updated = False
        hactivity.save()
        if self.request.user.has_perm('landmatrix.change_activity'):
            hactivity.update_public_activity()
        self.create_involvement(hactivity, investor_form)

        # Create activity feedback
        form = self.get_form_by_type(forms, DealActionCommentForm)
        if form:
            self.create_activity_feedback(hactivity, form)

        # Create success message
        if self.request.user.has_perm('landmatrix.change_activity'):
            messages.success(self.request, self.success_message_admin.format(hactivity.activity_identifier))
        else:
            self.create_activity_changeset(hactivity)
            messages.success(self.request, self.success_message.format(hactivity.activity_identifier))

        context = self.get_context_data(**self.kwargs)
        context['forms'] = forms
        return self.render_to_response(context)


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

            attributes = form.get_attributes(self.request)
            if not attributes:
                continue
            # Formset?
            if isinstance(attributes, list):
                # Loop forms
                for count, form_attributes in enumerate(attributes):
                    if form_attributes:
                        aag, created = ActivityAttributeGroup.objects.get_or_create(
                            name='%s_%02i' % (form.Meta.name, count), # two digits required for ordering
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

        return action_comment

    def create_involvement(self, activity, form):
        # FIXME
        # Problem here: Involvements are not historical yet, but activity and investors are.
        # As an intermediate solution we'll just create another involvement which links
        # to the public activity, which will replace the current involvement when the
        # historical activity gets approved.
        activity, created = Activity.objects.get_or_create(
            id=activity.id,
            activity_identifier=activity.activity_identifier
        )

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
        if operational_stakeholder:
            involvement = InvestorActivityInvolvement.objects.create(
                fk_activity=activity,
                fk_investor=operational_stakeholder,
                fk_status_id=activity.STATUS_PENDING,
            )
            involvement.save()

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
        except:
            user = None
        changeset = ActivityChangeset.objects.create(
            fk_activity=activity,
            fk_country=country,
            #fk_region=country and country.region
            fk_user=user,
        )
        return changeset


    def login_user(self, user):
        """
        Log in a user without requiring credentials (using ``login`` from
        ``django.contrib.auth``, first finding a matching backend).

        """
        from django.contrib.auth import load_backend, login
        if not hasattr(user, 'backend'):
            for backend in settings.AUTHENTICATION_BACKENDS:
                if user == load_backend(backend).get_user(user.pk):
                    user.backend = backend
                    break
        if hasattr(user, 'backend'):
            return login(self.request, user)