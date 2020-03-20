from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import (
    DetailView,
    FormView,
    ListView,
    RedirectView,
    TemplateView,
)

from apps.editor.forms import ApproveRejectChangeForm
from apps.editor.models import UserRegionalInfo
from apps.editor.utils import activity_or_investor_to_template, feedback_to_template
from apps.landmatrix.models import (
    ActivityFeedback,
    Country,
    HistoricalActivity,
    HistoricalInvestor,
)


class FilteredQuerySetMixin:
    def _get_countries(self):
        """
        Get allowed countries for logged in user
        :return:
        """
        try:
            user_regional_info = UserRegionalInfo.objects.get(user=self.request.user)
        except UserRegionalInfo.DoesNotExist:
            user_regional_info = None

        if "country" in self.request.GET:
            country_ids = self.request.GET.getlist("country")
            try:
                country_ids = filter(
                    None, [str(country_id) for country_id in country_ids]
                )
            except ValueError:  # pragma: no cover
                country_ids = []
        elif user_regional_info:
            country_ids = [
                str(id)
                for id in user_regional_info.country.values_list("id", flat=True)
            ]
        else:
            country_ids = []

        if "region" in self.request.GET:
            region_ids = self.request.GET.getlist("region")
            try:
                region_ids = filter(None, [str(region_id) for region_id in region_ids])
            except ValueError:  # pragma: no cover
                region_ids = []
        elif user_regional_info:
            region_ids = [
                str(id) for id in user_regional_info.region.values_list("id", flat=True)
            ]
        else:
            region_ids = []
        if region_ids:
            for region_id in region_ids:
                country_ids.extend(
                    [
                        str(country_id.id)
                        for country_id in Country.objects.filter(fk_region=region_id)
                    ]
                )
        return country_ids

    def get_filtered_activity_queryset(self, queryset=None):
        """
        Filter historical activities by country/region of logged in user
        :param queryset:
        :return:
        """
        if queryset is None:
            queryset = HistoricalActivity.objects.all()

        countries = self._get_countries()
        if countries:
            queryset = queryset.filter(
                attributes__name="target_country", attributes__value__in=countries
            )

        return queryset

    def get_filtered_investor_queryset(self, queryset=None):
        """
        Filter historical investors by country/region of logged in user
         (using target country of assigned deals)
        :param queryset:
        :return:
        """
        if queryset is None:
            queryset = HistoricalInvestor.objects.all()

        # Investor is not OC company
        filters = Q(involvements__isnull=True)

        countries = self._get_countries()
        if countries:
            # OR investor is OC company with newest deal version in one of the countries
            latest_ids = HistoricalActivity.objects.latest_ids()
            filters |= Q(
                involvements__fk_activity__attributes__name="target_country",
                involvements__fk_activity__attributes__value__in=countries,
                involvements__fk_activity_id__in=latest_ids,
            )

        return queryset.filter(filters)


class LatestQuerySetMixin(FilteredQuerySetMixin):
    def _get_activities_and_investors_list(self, filter, limit):
        activities = getattr(self.get_filtered_activity_queryset(), filter)()
        result = list(activities.filter(id__in=activities.latest_ids())[:limit])
        investors = getattr(self.get_filtered_investor_queryset(), filter)()
        result += list(investors.filter(id__in=investors.latest_ids())[:limit])
        result.sort(key=lambda p: p.history_date, reverse=True)
        return result[:limit]

    def get_latest_added_queryset(self, limit=None):
        return self._get_activities_and_investors_list("active", limit=limit)

    def get_latest_modified_queryset(self, limit=None):
        return self._get_activities_and_investors_list("overwritten", limit=limit)

    def get_latest_deleted_queryset(self, limit=None):
        return self._get_activities_and_investors_list("deleted", limit=limit)


class PendingChangesMixin(FilteredQuerySetMixin):
    def get_permitted_activities(self, queryset=None):
        if queryset is None:
            queryset = HistoricalActivity.objects.all()

        # for public users:
        if not self.request.user.has_perm("landmatrix.review_historicalactivity"):
            queryset = queryset.none()
        # for editors:
        # show only activites that have been added/changed by public users
        # and not been reviewed by another editor yet
        elif not self.request.user.has_perm("landmatrix.change_historicalactivity"):
            queryset = queryset.filter(history_user__groups__name="Reporters")
            queryset = queryset.exclude(changesets__fk_user__groups__name="Editors")
        # for admins:
        # show activities that have been added/changed or reviewed by editors or reporters
        # FIXME: Is filtering necessary here at all?
        else:
            # queryset = queryset.filter(Q(history_user__groups__name__in=('Reporters', 'Editors')) |
            #    Q(changesets__fk_user__groups__name__in=('Reporters', 'Editors')))
            pass  # No filter required for admins

        return queryset

    def get_permitted_investors(self, queryset=None):
        if queryset is None:
            queryset = HistoricalInvestor.objects.all()

        # for public users:
        if not self.request.user.has_perm("landmatrix.review_historicalactivity"):
            queryset = queryset.none()
        # for editors:
        # show only activites that have been added/changed by public users
        # and not been reviewed by another editor yet
        elif not self.request.user.has_perm("landmatrix.change_historicalactivity"):
            queryset = queryset.filter(history_user__groups__name="Reporters")
            # queryset = queryset.exclude(changesets__fk_user__groups__name='Editors')
        # for admins:
        # show activities that have been added/changed or reviewed by editors or reporters
        # FIXME: Is filtering necessary here at all?
        else:
            # queryset = queryset.filter(Q(history_user__groups__name__in=('Reporters', 'Editors')) |
            #    Q(changesets__fk_user__groups__name__in=('Reporters', 'Editors')))
            pass  # No filter required for admins

        return queryset

    def get_pending_adds_queryset(self, limit=None):
        activities = self.get_filtered_activity_queryset(
            queryset=self.get_permitted_activities()
        )
        activities = activities.without_multiple_revisions()
        activities = activities.pending_only()
        items = list(activities.distinct()[:limit])
        investors = self.get_filtered_investor_queryset(
            queryset=self.get_permitted_investors()
        )
        investors = investors.without_multiple_revisions()
        investors = investors.pending_only()
        items += list(investors.distinct()[:limit])
        items.sort(key=lambda i: i.history_date, reverse=True)
        return items[:limit]

    def get_pending_updates_queryset(self, limit=None):
        activities = self.get_filtered_activity_queryset(
            queryset=self.get_permitted_activities()
        )
        activities = activities.with_multiple_revisions()
        activities = activities.pending_only()
        items = list(activities.distinct()[:limit])
        investors = self.get_filtered_investor_queryset(
            queryset=self.get_permitted_investors()
        )
        investors = investors.with_multiple_revisions()
        investors = investors.pending_only()
        items += list(investors.distinct()[:limit])
        items.sort(key=lambda i: i.history_date, reverse=True)
        return items[:limit]

    def get_pending_deletes_queryset(self, limit=None):
        activities = self.get_filtered_activity_queryset(
            queryset=self.get_permitted_activities()
        )
        activities = activities.to_delete()
        items = list(
            activities.filter(id__in=activities.latest_ids()).distinct()[:limit]
        )
        investors = self.get_filtered_investor_queryset(
            queryset=self.get_permitted_investors()
        )
        investors = investors.to_delete()
        items += list(
            investors.filter(id__in=investors.latest_ids()).distinct()[:limit]
        )
        items.sort(key=lambda i: i.history_date, reverse=True)
        return items[:limit]

    def get_feedback_queryset(self):
        feedback = ActivityFeedback.objects.filter(
            fk_activity__id__in=HistoricalActivity.objects.latest_only()
        )
        feedback = feedback.filter(fk_user_assigned=self.request.user)
        return feedback

    def get_rejected_queryset(self, limit=None):
        activities = self.get_filtered_activity_queryset()
        activities = activities.rejected()
        activities = activities.filter(changesets__fk_user=self.request.user)
        items = list(
            activities.filter(id__in=activities.latest_ids()).distinct()[:limit]
        )
        investors = self.get_filtered_investor_queryset()
        investors = investors.rejected()
        # investors = investors.filter(changesets__fk_user=self.request.user)
        items += list(
            investors.filter(id__in=investors.latest_ids()).distinct()[:limit]
        )
        items.sort(key=lambda i: i.history_date, reverse=True)
        return items[:limit]

    def get_for_user_queryset(self, limit=None):
        items = list(
            HistoricalActivity.objects.get_for_user(self.request.user.id)[:limit]
        )
        items += list(
            HistoricalInvestor.objects.get_for_user(self.request.user.id)[:limit]
        )
        items.sort(key=lambda i: i.history_date, reverse=True)
        return items[:limit]


class DashboardView(LatestQuerySetMixin, PendingChangesMixin, TemplateView):
    template_name = "dashboard.html"
    paginate_by = 10

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # deal_count = Activity.objects.overall_activity_count()
        # public_count = Activity.objects.public_activity_count()
        # private_count = deal_count - public_count

        latest_added = self.get_latest_added_queryset(limit=self.paginate_by)
        latest_modified = self.get_latest_modified_queryset(limit=self.paginate_by)
        latest_deleted = self.get_latest_deleted_queryset(limit=self.paginate_by)

        # Merge and reorder pendings
        pendings = []
        for act_or_inv in self.get_pending_adds_queryset():
            pendings.append(
                {
                    "action": "add",
                    "act_inv": activity_or_investor_to_template(act_or_inv),
                }
            )
        for act_or_inv in self.get_pending_updates_queryset():
            pendings.append(
                {
                    "action": "update",
                    "act_inv": activity_or_investor_to_template(act_or_inv),
                }
            )
        for act_or_inv in self.get_pending_deletes_queryset():
            pendings.append(
                {
                    "action": "delete",
                    "act_inv": activity_or_investor_to_template(act_or_inv),
                }
            )
        pendings.sort(key=lambda p: p["act_inv"]["timestamp"], reverse=True)
        feedback = self.get_feedback_queryset()

        context.update(
            {
                # 'statistics': {
                #    'overall_deal_count': deal_count,
                #    'public_deal_count': public_count,
                #    'not_public_deal_count': private_count,
                # },
                "view": "dashboard",
                "latest_added": list(
                    map(activity_or_investor_to_template, latest_added)
                ),
                "latest_modified": list(
                    map(activity_or_investor_to_template, latest_modified)
                ),
                "latest_deleted": tuple(
                    map(activity_or_investor_to_template, latest_deleted)
                ),
                "manage": pendings[: self.paginate_by],
                "feedbacks": {
                    "feeds": list(
                        map(feedback_to_template, feedback[: self.paginate_by])
                    )
                },
                "filters": {
                    "country_ids": self.request.GET.getlist("country"),
                    "region_ids": self.request.GET.getlist("region"),
                },
            }
        )

        return context


class BaseLogView(LatestQuerySetMixin, ListView):
    template_name = "log.html"
    paginate_by = 50
    context_object_name = "items"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mapped_activities = list(
            map(activity_or_investor_to_template, context["items"])
        )
        context.update(
            {"view": "log", "action": self.action, "items": mapped_activities}
        )

        return context


class LogAddedView(BaseLogView):
    action = "latest_added"

    def get_queryset(self):
        return self.get_latest_added_queryset()


class LogModifiedView(BaseLogView):
    action = "latest_modified"

    def get_queryset(self):
        return self.get_latest_modified_queryset()


class LogDeletedView(BaseLogView):
    action = "latest_deleted"

    def get_queryset(self):
        return self.get_latest_deleted_queryset()


class ManageRootView(RedirectView):
    permanent = False
    query_string = True

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.has_perm("landmatrix.review_historicalactivity"):
            url = reverse("manage_feedback")
        else:
            url = reverse("manage_for_user")

        return url


class BaseManageView(PendingChangesMixin, ListView):
    template_name = "manage.html"
    paginate_by = 10
    context_object_name = "items"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @staticmethod
    def process_objects_for_template(object_list):
        return list(map(activity_or_investor_to_template, object_list))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        mapped_objects = self.process_objects_for_template(context["items"])

        context.update(
            {
                "view": "manage",
                "action": self.action,
                "items": mapped_objects,
                "pending_adds_count": len(self.get_pending_adds_queryset()),
                "pending_updates_count": len(self.get_pending_updates_queryset()),
                "pending_deletes_count": len(self.get_pending_deletes_queryset()),
                "feedback_count": len(self.get_feedback_queryset()),
                "rejected_count": len(self.get_rejected_queryset()),
                "for_user_count": len(self.get_for_user_queryset()),
                # TODO: investor deletes
                # 'investor_deletes_count': 0,
            }
        )

        return context


class ManageFeedbackView(BaseManageView):
    action = "feedback"

    @method_decorator(permission_required("landmatrix.review_historicalactivity"))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @staticmethod
    def process_objects_for_template(object_list):
        return list(map(feedback_to_template, object_list))

    def get_queryset(self):
        return self.get_feedback_queryset()


class ManageRejectedView(BaseManageView):
    action = "rejected"

    def get_queryset(self):
        return self.get_rejected_queryset()


class ManageAddsView(BaseManageView):
    action = "pending_adds"

    @method_decorator(permission_required("landmatrix.review_historicalactivity"))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.get_pending_adds_queryset()


class ManageUpdatesView(BaseManageView):
    action = "pending_updates"

    @method_decorator(permission_required("landmatrix.review_historicalactivity"))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.get_pending_updates_queryset()


class ManageDeletesView(BaseManageView):
    action = "pending_deletes"

    @method_decorator(permission_required("landmatrix.review_historicalactivity"))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.get_pending_deletes_queryset()


class ManageForUserView(BaseManageView):
    action = "for_user"

    def get_queryset(self):
        return self.get_for_user_queryset()


class BaseManageDealView(FormView, DetailView):
    template_name = "manage_item.html"
    form_class = ApproveRejectChangeForm
    model = HistoricalActivity
    pk_url_kwarg = "id"
    context_object_name = "item"

    @method_decorator(permission_required("landmatrix.review_historicalactivity"))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        if not hasattr(self, "object"):  # pragma: no cover
            self.object = self.get_object()

        context = super().get_context_data(**kwargs)
        context.update({"action": self.action, "form": self.get_form()})
        if hasattr(self.object, "activity_identifier"):
            context.update({"type": "activity", "id": self.object.activity_identifier})
        else:
            context.update({"type": "investor", "id": self.object.investor_identifier})

        return context

    def redirect_with_message(self, message):
        messages.success(self.request, message)

        return HttpResponseRedirect(reverse("manage_feedback"))


class ApproveActivityChangeView(BaseManageDealView):
    queryset = HistoricalActivity.objects.pending_only()
    action = "approve"

    def form_valid(self, form):
        activity = self.get_object()
        activity.approve_change(
            user=self.request.user, comment=form.cleaned_data["tg_action_comment"]
        )

        return self.redirect_with_message(_("Deal has been successfully approved."))


class RejectActivityChangeView(BaseManageDealView):
    queryset = HistoricalActivity.objects.pending_only()
    action = "reject"

    def form_valid(self, form):
        activity = self.get_object()
        activity.reject_change(
            user=self.request.user, comment=form.cleaned_data["tg_action_comment"]
        )

        return self.redirect_with_message(_("Deal has been successfully rejected."))


class ApproveActivityDeleteView(BaseManageDealView):
    queryset = HistoricalActivity.objects.to_delete()
    action = "approve"

    # @method_decorator(permission_required('landmatrix.delete_activity'))
    # def dispatch(self, *args, **kwargs):
    #    return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        activity = self.get_object()
        activity.approve_delete(
            user=self.request.user, comment=form.cleaned_data["tg_action_comment"]
        )

        return self.redirect_with_message(
            _("Deal deletion has been successfully approved.")
        )


class RejectActivityDeleteView(BaseManageDealView):
    queryset = HistoricalActivity.objects.to_delete()
    action = "reject"

    # @method_decorator(permission_required('landmatrix.delete_activity'))
    # def dispatch(self, *args, **kwargs):
    #    return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        activity = self.get_object()
        activity.reject_delete(
            user=self.request.user, comment=form.cleaned_data["tg_action_comment"]
        )

        return self.redirect_with_message(
            _("Deal deletion has been successfully rejected.")
        )


class BaseManageInvestorView(BaseManageDealView):
    model = HistoricalInvestor


class ApproveInvestorChangeView(BaseManageInvestorView):
    queryset = HistoricalInvestor.objects.pending_only()
    action = "approve"

    def form_valid(self, form):
        investor = self.get_object()
        investor.approve_change(
            user=self.request.user, comment=form.cleaned_data["tg_action_comment"]
        )

        return self.redirect_with_message(_("Investor has been successfully approved."))


class RejectInvestorChangeView(BaseManageInvestorView):
    queryset = HistoricalInvestor.objects.pending_only()
    action = "reject"

    def form_valid(self, form):
        investor = self.get_object()
        investor.reject_change(
            user=self.request.user, comment=form.cleaned_data["tg_action_comment"]
        )

        return self.redirect_with_message(_("Investor has been successfully rejected."))


class ApproveInvestorDeleteView(BaseManageInvestorView):
    queryset = HistoricalInvestor.objects.to_delete()
    action = "approve"

    # @method_decorator(permission_required('landmatrix.delete_investor'))
    # def dispatch(self, *args, **kwargs):
    #    return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        activity = self.get_object()
        activity.approve_delete(
            user=self.request.user, comment=form.cleaned_data["tg_action_comment"]
        )

        return self.redirect_with_message(
            _("Investor deletion has been successfully approved.")
        )


class RejectInvestorDeleteView(BaseManageInvestorView):
    queryset = HistoricalInvestor.objects.to_delete()
    action = "reject"

    # @method_decorator(permission_required('landmatrix.delete_investor'))
    # def dispatch(self, *args, **kwargs):
    #    return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        activity = self.get_object()
        activity.reject_delete(
            user=self.request.user, comment=form.cleaned_data["tg_action_comment"]
        )

        return self.redirect_with_message(
            _("Investor deletion has been successfully rejected.")
        )
