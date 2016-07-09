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
from landmatrix.models.investor import InvestorActivityInvolvement
from landmatrix.models.language import Language
from landmatrix.models.status import Status
from landmatrix.models.activity_changeset import ActivityChangeset
from landmatrix.models.activity_feedback import ActivityFeedback
from grid.forms.public_user_information_form import PublicUserInformationForm
from editor.models import UserRegionalInfo

from django.views.generic import TemplateView

from django.db import transaction
from django.contrib import messages
from django.core.exceptions import MultipleObjectsReturned
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from django.utils.text import slugify

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
                user_information = forms[-1]
                if not isinstance(user_information, PublicUserInformationForm):
                    raise IOError(_('User is not authenticated and not user information given.'))
                data = user_information.cleaned_data
                names = data.get('public_user_name', '').split(' ')
                try:
                    user = User.objects.get(email=data.get('public_user_email'))
                except:
                    user = User.objects.create(
                        username=data.get('public_user_email'),
                        email=data.get('public_user_email'),
                        first_name=' '.join(names[:-1]),
                        last_name=names[-1],
                    )
                    UserRegionalInfo.objects.create(
                        user=user,
                        phone=data.get('public_user_phone'),
                    )
                    group, created = Group.objects.get_or_create(name='Reporters')
                    user.groups.add(group)
                self.request.user = user
            return self.form_valid(forms)
        else:
            return self.form_invalid(forms)

    def form_valid(self, forms):
        hactivity = self.get_object()
        investor_form = list(filter(lambda f: isinstance(f, OperationalStakeholderForm), forms))[0]
        # Create new historical activity
        hactivity.pk = None
        hactivity.history_user = self.request.user
        hactivity.history_date = datetime.now()
        hactivity.save()
        # Create new activity attributes
        hactivity.comment = self.create_attributes(hactivity, forms)
        hactivity.fully_updated = self.get_fully_updated(forms[-1])
        hactivity.save()
        hactivity.update_public_activity()
        self.create_involvement(hactivity, investor_form)

        # Create activity feedback
        self.create_activity_feedback(hactivity, forms[-1])

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
        involvement = InvestorActivityInvolvement.objects.create(
            fk_activity=activity,
            fk_investor=operational_stakeholder,
            fk_status_id=activity.STATUS_PENDING,
        )
        involvement.save()

    def create_activity_feedback(self, activity, form):
        if self.request.user.is_authenticated():
            if not isinstance(form, DealActionCommentForm):
                # Public user
                return
            data = form.cleaned_data
            if data.get('assign_to_user', None):
                feedback = ActivityFeedback.objects.create(
                    fk_activity_id=self.get_object().id,
                    fk_user_assigned=data.get('assign_to_user'),
                    fk_user_created=self.request.user,
                    comment=data.get('tg_feedback_comment'),
                )

    def get_fully_updated(self, form):
        if self.request.user.is_authenticated():
            if not isinstance(form, DealActionCommentForm):
                # Public user
                return False
            return form.cleaned_data.get('fully_updated', False)
        return False

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
