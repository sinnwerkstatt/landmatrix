from django.utils.translation import ugettext_lazy as _
from django.db.models import Max
from django.db import transaction
from django.contrib import messages

from grid.views.save_deal_view import SaveDealView
from landmatrix.models.activity import Activity, HistoricalActivity
from landmatrix.models.activity_changeset import ActivityChangeset
from grid.forms.operational_stakeholder_form import OperationalStakeholderForm
from grid.forms.public_user_information_form import PublicUserInformationForm
from grid.forms.deal_action_comment_form import DealActionCommentForm

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class AddDealView(SaveDealView):
    template_name = 'add-deal.html'
    success_message = _('Added successfully.')

    def get_forms(self, data=None, files=None):
        forms = []
        for form_class in self.FORMS:
            # Add register form instead of action comment form for non authenticated user
            if form_class == DealActionCommentForm and not self.request.user.is_authenticated():
                forms.append(PublicUserInformationForm(data=data))
            else:
                prefix = hasattr(form_class.Meta, 'name') and form_class.Meta.name or None
                forms.append(form_class(data=data, files=files, prefix=prefix))
        return forms

    def form_valid(self, forms):
        activity_identifier = Activity.objects.values().aggregate(Max('activity_identifier'))['activity_identifier__max'] + 1
        investor_form = list(filter(lambda f: isinstance(f, OperationalStakeholderForm), forms))[0]
        # Create new historical activity
        hactivity = HistoricalActivity(
            activity_identifier=activity_identifier,
            history_user=self.request.user,
        )
        if not self.request.user.is_superuser:
            hactivity.fk_status_id = 1
        hactivity.save()
        # Create new activity attributes
        action_comment = self.create_attributes(hactivity, forms)
        # Create new activity (required for involvement)
        activity = Activity(
            activity_identifier=activity_identifier,
        )
        if not self.request.user.is_superuser:
            activity.fk_status_id = 1
        activity.save()
        self.create_involvement(hactivity, investor_form)
        # Create changeset
        changeset = ActivityChangeset.objects.create(
            fk_activity=hactivity,
            comment=action_comment
        )
        messages.success(self.request, self.success_message.format(self.deal_id))

        context = self.get_context_data(**kwargs)
        context['forms'] = forms
        return self.render_to_response(context)