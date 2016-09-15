from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import (
    TemplateView, RedirectView, ListView, DetailView, FormView,
)

from landmatrix.models import Activity, HistoricalActivity, ActivityFeedback
from editor.forms import ApproveRejectChangeForm
from editor.filters import filter_activity_queryset, filter_managed_activities
from editor.utils import activity_to_template, feedback_to_template


class LatestActivitiesMixin:

    def get_latest_added_queryset(self):
        latest_added = HistoricalActivity.objects.active()
        latest_added = filter_activity_queryset(self.request, latest_added)

        return latest_added

    def get_latest_modified_queryset(self):
        latest_modified = HistoricalActivity.objects.overwritten()
        latest_modified = filter_activity_queryset(
            self.request, latest_modified)

        return latest_modified

    def get_latest_deleted_queryset(self):
        latest_deleted = HistoricalActivity.objects.deleted()
        latest_deleted = filter_activity_queryset(self.request, latest_deleted)

        return latest_deleted


class PendingChangesMixin:

    def get_pending_adds_queryset(self):
        inserts = HistoricalActivity.objects.without_multiple_revisions()
        inserts = inserts.pending_only()
        inserts = filter_activity_queryset(self.request, inserts)
        inserts = filter_managed_activities(self.request.user, inserts)

        return inserts

    def get_pending_updates_queryset(self):
        updates = HistoricalActivity.objects.with_multiple_revisions()
        updates = updates.pending_only()
        updates = filter_activity_queryset(self.request, updates)
        updates = filter_managed_activities(self.request.user, updates)

        return updates

    def get_pending_deletes_queryset(self):
        deletes = HistoricalActivity.objects.to_delete()
        deletes = filter_activity_queryset(self.request, deletes)
        deletes = filter_managed_activities(self.request.user, deletes)

        return deletes

    def get_feedback_queryset(self):
        feedback = ActivityFeedback.objects.active()
        feedback = feedback.filter(fk_user_assigned=self.request.user)

        return feedback

    def get_pending_investor_deletes_queryset(self):
        raise NotImplementedError  # TODO: implement

    def get_rejected_queryset(self):
        rejected = HistoricalActivity.objects.rejected()
        rejected = rejected.filter(changesets__fk_user=self.request.user)
        rejected = filter_activity_queryset(self.request, rejected)
        rejected = filter_managed_activities(self.request.user, rejected)

        return rejected

    def get_my_deals_queryset(self):
        my_deals = HistoricalActivity.objects.get_my_deals(
            self.request.user.id)
        my_deals = filter_activity_queryset(self.request, my_deals)
        my_deals = filter_managed_activities(self.request.user, my_deals)

        return my_deals


class DashboardView(LatestActivitiesMixin, PendingChangesMixin, TemplateView):
    template_name = 'dashboard.html'
    paginate_by = 10

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        deal_count = Activity.objects.overall_activity_count()
        public_count = Activity.objects.public_activity_count()
        private_count = deal_count - public_count

        latest_added = self.get_latest_added_queryset()
        latest_modified = self.get_latest_modified_queryset()
        latest_deleted = self.get_latest_deleted_queryset()
        pending_adds = self.get_pending_adds_queryset()
        pending_updates = self.get_pending_updates_queryset()
        pending_deletes = self.get_pending_deletes_queryset()
        feedback = self.get_feedback_queryset()

        context.update({
            'statistics': {
                'overall_deal_count': deal_count,
                'public_deal_count': public_count,
                'not_public_deal_count': private_count,
            },
            'view': 'dashboard',
            'latest_added': map(
                activity_to_template, latest_added[:self.paginate_by]),
            'latest_modified': map(
                activity_to_template, latest_modified[:self.paginate_by]),
            'latest_deleted': map(
                activity_to_template, latest_deleted[:self.paginate_by]),
            'manage': {
                'activities': {
                    'inserts': map(
                        activity_to_template, pending_adds[:self.paginate_by]),
                    'updates': map(
                        activity_to_template,
                        pending_updates[:self.paginate_by]),
                    'deletes': map(
                        activity_to_template,
                        pending_deletes[:self.paginate_by]),
                }
            },
            'feedbacks': {
                'feeds': map(feedback_to_template, feedback[:self.paginate_by])
            },
        })

        return context


class BaseLogView(LatestActivitiesMixin, ListView):
    template_name = 'log.html'
    paginate_by = 50
    context_object_name = 'activities'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mapped_activities = map(activity_to_template, context['activities'])
        context.update({
            'view': 'log',
            'action': self.action,
            'activities': mapped_activities,
        })

        return context


class LogAddedView(BaseLogView):
    action = 'latest_added'

    def get_queryset(self):
        return self.get_latest_added_queryset()


class LogModifiedView(BaseLogView):
    action = 'latest_modified'

    def get_queryset(self):
        return self.get_latest_modified_queryset()


class LogDeletedView(BaseLogView):
    action = 'latest_deleted'

    def get_queryset(self):
        return self.get_latest_deleted_queryset()


class ManageRootView(RedirectView):
    permanent = False
    query_string = True

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.has_perm('landmatrix.review_activity'):
            url = reverse('manage_feedback')
        else:
            url = reverse('manage_my_deals')

        return url


class BaseManageView(PendingChangesMixin, ListView):
    template_name = 'manage.html'
    paginate_by = 10
    context_object_name = 'activities'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def process_objects_for_template(self, object_list):
        return map(activity_to_template, object_list)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        mapped_objects = self.process_objects_for_template(
            context['activities'])

        context.update({
            'view': 'manage',
            'action': self.action,
            'activities': mapped_objects,
            'pending_adds_count': self.get_pending_adds_queryset().count(),
            'pending_updates_count': self.get_pending_updates_queryset().count(),
            'pending_deletes_count': self.get_pending_deletes_queryset().count(),
            'feedback_count': self.get_feedback_queryset().count(),
            'rejected_count': self.get_rejected_queryset().count(),
            'my_deals_count': self.get_my_deals_queryset().count(),
            # TODO: investor deletes
            # 'investor_deletes_count': 0,
        })

        return context


class ManageFeedbackView(BaseManageView):
    action = 'feedback'

    @method_decorator(permission_required('landmatrix.review_activity'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def process_objects_for_template(self, object_list):
        return map(feedback_to_template, object_list)

    def get_queryset(self):
        return self.get_feedback_queryset()


class ManageRejectedView(BaseManageView):
    action = 'rejected'

    def get_queryset(self):
        return self.get_rejected_queryset()


class ManageAddsView(BaseManageView):
    action = 'pending_adds'

    @method_decorator(permission_required('landmatrix.review_activity'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return self.get_pending_adds_queryset()


class ManageUpdatesView(BaseManageView):
    action = 'pending_updates'

    @method_decorator(permission_required('landmatrix.review_activity'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return self.get_pending_updates_queryset()


class ManageDeletesView(BaseManageView):
    action = 'pending_deletes'

    @method_decorator(permission_required('landmatrix.review_activity'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return self.get_pending_deletes_queryset()


class ManageInvestorDeletesView(BaseManageView):
    action = 'investor_deletes'

    @method_decorator(permission_required('landmatrix.review_activity'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return self.get_pending_investor_deletes_queryset()


class ManageMyDealsView(BaseManageView):
    action = 'my_deals'

    def get_queryset(self):
        return self.get_my_deals_queryset()


class BaseManageDealView(FormView, DetailView):
    template_name = 'manage_item.html'
    form_class = ApproveRejectChangeForm
    model = HistoricalActivity
    pk_url_kwarg = 'id'
    context_object_name = 'activity'

    @method_decorator(permission_required('landmatrix.review_activity'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        if not hasattr(self, 'object'):
            self.object = self.get_object()

        context = super().get_context_data(**kwargs)
        context.update({
            'action': self.action,
            'form': self.get_form(),
        })

        return context

    def redirect_with_message(self, message):
        messages.success(self.request, message)

        return HttpResponseRedirect(reverse('manage_feedback'))


class ApproveActivityChangeView(BaseManageDealView):
    queryset = HistoricalActivity.objects.pending_only()
    action = 'approve'

    def form_valid(self, form):
        activity = self.get_object()
        activity.approve_change(
            user=self.request.user,
            comment=form.cleaned_data['tg_action_comment'])

        return self.redirect_with_message(
            _("Deal has been successfully approved."))


class RejectActivityChangeView(BaseManageDealView):
    queryset = HistoricalActivity.objects.pending_only()
    action = 'reject'

    def form_valid(self, form):
        activity = self.get_object()
        activity.reject_change(
            user=self.request.user,
            comment=form.cleaned_data['tg_action_comment'])

        return self.redirect_with_message(
            _("Deal has been successfully rejected."))


class ApproveActivityDeleteView(BaseManageDealView):
    queryset = HistoricalActivity.objects.to_delete()
    action = 'approve'

    @method_decorator(permission_required('landmatrix.delete_activity'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        activity = self.get_object()
        activity.approve_delete(
            user=self.request.user,
            comment=form.cleaned_data['tg_action_comment'])

        return self.redirect_with_message(
            _("Deal deletion has been successfully approved."))


class RejectActivityDeleteView(BaseManageDealView):
    queryset = HistoricalActivity.objects.to_delete()
    action = 'reject'

    @method_decorator(permission_required('landmatrix.delete_activity'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        activity = self.get_object()
        activity.reject_delete(
            user=self.request.user,
            comment=form.cleaned_data['tg_action_comment'])

        return self.redirect_with_message(
            _("Deal deletion has been successfully rejected."))


# TODO: investor approve/reject
