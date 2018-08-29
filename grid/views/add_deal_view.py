from django.utils.translation import ugettext_lazy as _
from django.db.models import Max
from django.db import transaction
from django.contrib import messages
from django.forms.formsets import BaseFormSet
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from grid.views.save_deal_view import SaveDealView
from landmatrix.models.activity import Activity, HistoricalActivity
from landmatrix.models.activity_changeset import ActivityChangeset
from grid.forms.operational_stakeholder_form import OperationalStakeholderForm
from grid.forms.public_user_information_form import PublicUserInformationForm
from grid.forms.deal_action_comment_form import DealActionCommentForm
from grid.utils import has_perm_approve_reject


class AddDealView(SaveDealView):
    template_name = 'add-deal.html'
    success_message = _('Added successfully.')
    success_message = _('The deal has been submitted successfully (#{}). It will be reviewed and published soon.')
    success_message_admin = _('The deal has been added successfully (#{}).')

    def get_forms(self, data=None, files=None):
        forms = []
        for form_class in self.FORMS:
            prefix = issubclass(form_class, BaseFormSet) and form_class.Meta.name or None
            forms.append(form_class(data=data, files=files, prefix=prefix))
        return forms

    def form_valid(self, forms):
        activity_identifier = HistoricalActivity.objects.values().aggregate(Max('activity_identifier'))['activity_identifier__max'] or 0
        activity_identifier += 1
        investor_form = list(filter(lambda f: isinstance(f, OperationalStakeholderForm), forms))[0]
        # Create new historical activity
        hactivity = HistoricalActivity(
            activity_identifier=activity_identifier,
            history_user=self.request.user,
        )
        is_admin = self.request.user.has_perm('landmatrix.add_activity')
        hactivity.fk_status_id = hactivity.STATUS_PENDING
        hactivity.save()

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

        if is_admin:
            redirect_url = reverse(
                'deal_detail', kwargs={'deal_id': hactivity.activity_identifier})
        else:
            self.create_activity_changeset(hactivity)
            # TODO: check that is is correct, but all deals seems like a
            # reasonable place to redirect to, as these users can't see the
            # deal yet
            redirect_url = reverse('data')

        if 'approve_btn' in self.request.POST and has_perm_approve_reject(self.request.user, hactivity):
            messages.success(
                self.request,
                self.success_message_admin.format(hactivity.activity_identifier))
            hactivity.approve_change(self.request.user, '')
        elif 'reject_btn' in self.request.POST and has_perm_approve_reject(self.request.user, hactivity):
            hactivity.reject_change(self.request.user, '')
        else:
            messages.success(
                self.request,
                self.success_message.format(hactivity.activity_identifier))

        return HttpResponseRedirect(redirect_url)
