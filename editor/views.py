from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import (
    TemplateView, RedirectView, ListView, DetailView, FormView,
)
from django.db.models import Q

from landmatrix.models import Activity, HistoricalActivity, ActivityFeedback, Country
from editor.models import UserRegionalInfo
from editor.forms import ApproveRejectChangeForm
from editor.utils import activity_to_template, feedback_to_template


class FilteredQuerysetMixin:

    def get_filtered_activity_queryset(self, queryset=None):
        '''
        Support for country and region filters.
        '''
        if queryset is None:
            queryset = HistoricalActivity.objects.all()

        try:
            user_regional_info = UserRegionalInfo.objects.get(
                user=self.request.user)
        except UserRegionalInfo.DoesNotExist:
            user_regional_info = None

        if 'country' in self.request.GET:
            country_ids = self.request.GET.getlist('country')
            try:
                country_ids = filter(
                    None, [str(country_id) for country_id in country_ids])
            except ValueError:
                country_ids = []
        elif user_regional_info:
            country_ids = [str(id) for id in user_regional_info.country.values_list('id', flat=True)]
        else:
            country_ids = []

        if 'region' in self.request.GET:
            region_ids = self.request.GET.getlist('region')
            try:
                region_ids = filter(
                    None, [str(region_id) for region_id in region_ids])
            except ValueError:
                region_ids = []
        elif user_regional_info:
            region_ids = [str(id) for id in user_regional_info.region.values_list('id', flat=True)]
        else:
            region_ids = []
        if region_ids:
            for region_id in region_ids:
                country_ids.extend(
                    [str(country_id.id) for country_id in Country.objects.filter(fk_region=region_id)]
                )

        if country_ids:
            queryset = queryset.filter(
                attributes__name='target_country',
                attributes__value__in=country_ids
            )

        return queryset


class LatestActivitiesMixin(FilteredQuerysetMixin):

    def get_latest_added_queryset(self):
        added = self.get_filtered_activity_queryset().active()
        return added.filter(id__in=added.latest_only())

    def get_latest_modified_queryset(self):
        modified = self.get_filtered_activity_queryset().overwritten()
        return modified.filter(id__in=modified.latest_only())

    def get_latest_deleted_queryset(self):
        deleted = self.get_filtered_activity_queryset().deleted()
        return deleted.filter(id__in=deleted.latest_only())


class PendingChangesMixin(FilteredQuerysetMixin):

    def get_permitted_activities(self, queryset=None):
        if queryset is None:
            queryset = HistoricalActivity.objects.all()

        # for public users:
        if not self.request.user.has_perm('landmatrix.review_activity'):
            queryset = queryset.none()
        # for editors:
        # show only activites that have been added/changed by public users
        # and not been reviewed by another editor yet
        elif not self.request.user.has_perm('landmatrix.change_activity'):
            queryset = queryset.filter(history_user__groups__name='Reporters')
            queryset = queryset.exclude(changesets__fk_user__groups__name='Editors')
        # for admins:
        # show activities that have been added/changed or reviewed by editors or reporters
        # FIXME: Is filtering necessary here at all?
        else:
            #queryset = queryset.filter(Q(history_user__groups__name__in=('Reporters', 'Editors')) |
            #    Q(changesets__fk_user__groups__name__in=('Reporters', 'Editors')))
            pass # No filter required for admins

        return queryset

    def get_pending_adds_queryset(self):
        inserts = self.get_filtered_activity_queryset(
            queryset=self.get_permitted_activities())
        inserts = inserts.without_multiple_revisions()
        inserts = inserts.pending_only()
        return inserts.distinct()

    def get_pending_updates_queryset(self):
        updates = self.get_filtered_activity_queryset(
            queryset=self.get_permitted_activities())
        updates = updates.with_multiple_revisions()
        updates = updates.pending_only()
        return updates.distinct()

    def get_pending_deletes_queryset(self):
        deletes = self.get_filtered_activity_queryset(
            queryset=self.get_permitted_activities())
        deletes = deletes.to_delete()
        return deletes.filter(id__in=deletes.latest_only())

    def get_feedback_queryset(self):
        feedback = ActivityFeedback.objects.active()
        feedback = feedback.filter(fk_user_assigned=self.request.user)
        return feedback

    def get_pending_investor_deletes_queryset(self):
        raise NotImplementedError  # TODO: implement

    def get_rejected_queryset(self):
        rejected = self.get_filtered_activity_queryset()
        rejected = rejected.rejected()
        rejected = rejected.filter(changesets__fk_user=self.request.user)
        return rejected.filter(id__in=rejected.latest_only())

    def get_my_deals_queryset(self):
        my_deals = HistoricalActivity.objects.get_my_deals(self.request.user.id)
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
            #'statistics': {
            #    'overall_deal_count': deal_count,
            #    'public_deal_count': public_count,
            #    'not_public_deal_count': private_count,
            #},
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
            'filters': {
                'country_ids': self.request.GET.getlist('country'),
                'region_ids': self.request.GET.getlist('region'),
            }
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

    #@method_decorator(permission_required('landmatrix.delete_activity'))
    #def dispatch(self, *args, **kwargs):
    #    return super().dispatch(*args, **kwargs)

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

    #@method_decorator(permission_required('landmatrix.delete_activity'))
    #def dispatch(self, *args, **kwargs):
    #    return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        activity = self.get_object()
        activity.reject_delete(
            user=self.request.user,
            comment=form.cleaned_data['tg_action_comment'])

        return self.redirect_with_message(
            _("Deal deletion has been successfully rejected."))


# TODO: investor approve/reject
