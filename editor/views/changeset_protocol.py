from datetime import timedelta
from pprint import pprint
from traceback import print_stack

from django.utils.encoding import force_text

from editor.models import UserRegionalInfo
from grid.views.activity_protocol import ActivityProtocol
from landmatrix.models.activity import Activity, HistoricalActivity
from landmatrix.models.activity_attribute_group import ActivityAttribute
from landmatrix.models.activity_feedback import ActivityFeedback
from landmatrix.models.activity_changeset import ActivityChangeset, ReviewDecision

from django.views.generic import View
from django.http.response import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
import json

from landmatrix.models.country import Country
from landmatrix.models.investor import InvestorActivityInvolvement, InvestorVentureInvolvement, \
    Investor
from landmatrix.models.status import Status

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class ChangesetProtocol(View):

    DEFAULT_MAX_NUM_CHANGESETS = 100

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):

        self.request = request

        if "action" in kwargs:
            action = kwargs["action"]
        else:
            raise IOError("Parameter 'action' missing")

        if request.POST:
            self.data = json.loads(request.POST["data"])
        elif action in ('history', 'list'):
            self.data = {}
        else:
            raise IOError("Parameters missing")

        if action == "dashboard":
            return self.dashboard(request)
        elif action == "list":
            return self.list(request, *args, **kwargs)
        elif action == "approve":
            return self.approve(request, *args, **kwargs)
        elif action == "reject":
            return self.reject(request, *args, **kwargs)
        else:
            raise IOError("Unknown action")

    def dashboard(self, request):
        res = {
            "latest_added": self.get_paged_results(
                self.apply_dashboard_filters(HistoricalActivity.objects.filter(fk_status_id=Activity.STATUS_ACTIVE))[:self.DEFAULT_MAX_NUM_CHANGESETS],
                request.GET.get('latest_added_page')
            ),
            "latest_modified": self.get_paged_results(
                self.apply_dashboard_filters(HistoricalActivity.objects.filter(fk_status_id=Activity.STATUS_OVERWRITTEN))[:self.DEFAULT_MAX_NUM_CHANGESETS],
                request.GET.get('latest_modified_page')
            ),
            "latest_deleted": self.get_paged_results(
                self.apply_dashboard_filters(HistoricalActivity.objects.filter(fk_status_id=Activity.STATUS_DELETED))[:self.DEFAULT_MAX_NUM_CHANGESETS],
                request.GET.get('latest_deleted_page')
            ),
            "manage": self._activity_to_json(limit=2),
            "feedbacks": _feedbacks_to_json(request.user, limit=5),
            "rejected": _rejected_to_json(request.user)

        }
        return HttpResponse(json.dumps(res), content_type="application/json")

    def list(self, request, *args, **kwargs):
        """
        POST params:
            "activities": ["updates", "deletes", "inserts"]
            "sh_changesets": ["updates", "deletes", "inserts"]
        """
        user = request.user
        if user.has_perm("editor.change_activity"):
            self.data = {
                "activities": ["updates", "deletes", "inserts"],
                "sh_changesets": ["deletes"],
            }
        else:
            self.data = {
                "activities": ["my_deals"],
            }
        res = self._activity_to_json(
            user,
            request.GET.get('my_deals_page'), request.GET.get('updates_page'),
            request.GET.get('inserts_page'), request.GET.get('deletions_page')
        )
        res["feedbacks"] = _feedbacks_to_json(user, request.GET.get('feedbacks_page'))
        res["rejected"] = _rejected_to_json(request.user)

        return HttpResponse(json.dumps(res), content_type="application/json")

    @transaction.atomic
    def approve(self, request, *args, **kwargs):
        res = {"errors": []}
        self._approve_activities(request)
        _approve_investor_changes(request)
        return HttpResponse(json.dumps(res), content_type="application/json")

    def _approve_activities(self, request):
        for cs in self.data.get("activities", {}):
            changeset = ActivityChangeset.objects.get(id=cs.get("id"))
            activity = changeset.fk_activity
            if activity.fk_status_id == activity.STATUS_PENDING:
                _approve_activity_change(activity, changeset, cs.get("comment"), request)
            elif activity.fk_status_id == activity.STATUS_TO_DELETE:
                _approve_activity_deletion(activity, changeset, cs.get("comment"), request)

            _approve_investor_changes(get_activity_investor(activity), changeset)

    @transaction.atomic
    def reject(self, request, *args, **kwargs):
        res = {"errors": []}
        print('reject:', self.data)
        self._reject_activities(request)
        _reject_investor_changes(request)
        return HttpResponse(json.dumps(res), content_type="application/json")

    def _reject_activities(self, request):
        for cs in self.data.get("activities", {}):
            changeset = ActivityChangeset.objects.get(id=cs.get("id"))
            activity = changeset.fk_activity
            if activity.fk_status_id in (activity.STATUS_PENDING, activity.STATUS_TO_DELETE):
                _reject_activity_change(activity, changeset, cs.get('comment'), request)
            _reject_investor_changes(get_activity_investor(activity))

    def get_paged_results(self, records, page_number, per_page=10):
        paginator = Paginator(records, per_page)
        page = _get_page(page_number, paginator)

        results = {"cs": []}
        for changeset in page.object_list:
            results["cs"].append(self.changeset_template_data(changeset))
        # results["pagination"] = self._pagination_to_json(paginator, page)
        return results

    def changeset_template_data(self, activity, extra_data=None):
        if activity:
            try:
                user = activity.history_user.username
            except:
                # User doesn't exist anymore
                user = force_text(_("Deleted User"))
            template_data = {
                'id': activity.pk,
                "deal_id": activity.activity_identifier,
                "user": user,
                "timestamp": activity.history_date.strftime("%Y-%m-%d %H:%M:%S"),
                "comment": activity.comment,
            }
        else:
            template_data = {
                'id': 0,
                "deal_id": 0,
                "user": force_text(_("Public User")),
                "timestamp": 0,
                "comment": activity.comment
            }
        if extra_data:
            template_data.update(extra_data)

        return template_data

    def _activity_to_json(self, user=None, my_deals_page=1, updates_page=1, inserts_page=1, deletions_page=1, limit=None):
        res = {}
        if not self.data:
            self.data = {
                "activities": ["updates", "deletes", "inserts"],
                #"sh_changesets": ["deletes"],
            }
        if "activities" in self.data:
            self.handle_activities(deletions_page, inserts_page, limit, my_deals_page, res, updates_page, user)
        # print('_activity_to_json'); pprint(res)
        return res

    def apply_dashboard_filters(self, activities):
        if self.request.session.get('dashboard_filters', {}).get('country'):
            activities = _filter_activities_by_countries(
                activities, self.request.session['dashboard_filters']['country']
            )
        elif self.request.session.get('dashboard_filters', {}).get('region'):
            country_ids = Country.objects.filter(
                fk_region_id__in=self.request.session.get('dashboard_filters', {}).get('region')
            ).values_list('id', flat=True).distinct()
            activities = _filter_activities_by_countries(activities, [str(c) for c in country_ids])
        elif self.request.session.get('dashboard_filters', {}).get('user'):
            user = self.request.session.get('dashboard_filters', {}).get('user')
            if isinstance(user, list) and len(user):
                user = user[0]
            if UserRegionalInfo.objects.filter(user_id=user).exists():
                country = UserRegionalInfo.objects.get(user_id=user).country.all()
                if len(country):
                    activities = _filter_activities_by_countries(activities, [c.id for c in country])

        return _uniquify_activities_by_deal(activities)

    def handle_activities(self, deletions_page, inserts_page, limit, my_deals_page, res, updates_page, user):
        activities = {}
        if "my_deals" in self.data["activities"]:
            self.handle_my_deals(activities, limit, my_deals_page, user)
        if "updates" in self.data["activities"]:
            self.handle_updates(activities, limit, updates_page)
        if "inserts" in self.data["activities"]:
            self.handle_inserts(activities, limit, inserts_page)
        if "deletes" in self.data["activities"]:
            self.handle_deletes(activities, limit, deletions_page)
        if activities:
            _uniquify_changesets_dict(activities)
            res["activities"] = activities

    def handle_my_deals(self, activities, limit, my_deals_page, user):
        activities_my_deals = activities.get_my_deals(user.id)
        activities_my_deals = self.apply_dashboard_filters(activities_my_deals)
        activities_my_deals = limit and activities_my_deals[:limit] or activities_my_deals
        paginator = Paginator(activities_my_deals, 10)
        page = _get_page(my_deals_page, paginator)
        activities_my_deals = page.object_list
        my_deals = {"cs": []}
        for changeset in activities_my_deals:
            my_deals["cs"].append(self.changeset_template_data(changeset, {"status": changeset.fk_activity.fk_status.name}))
        if my_deals["cs"]:
            my_deals["pagination"] = _pagination_to_json(paginator, page)
            activities["my_deals"] = my_deals

    def handle_updates(self, activities, limit, updates_page):
        activities_update = HistoricalActivity.objects.filter(fk_status_id=HistoricalActivity.STATUS_PENDING)
        activities_update = self.apply_dashboard_filters(activities_update)
        activities_update = limit and activities_update[:limit] or activities_update
        paginator = Paginator(activities_update, 10)
        page = _get_page(updates_page, paginator)
        activities_update = page.object_list
        updates = {"cs": []}
        for changeset in activities_update:
            fields_changed = _find_changed_fields(changeset)
            updates["cs"].append(self.changeset_template_data(changeset, {"fields_changed": fields_changed}))
        if updates["cs"]:
            updates["pagination"] = _pagination_to_json(paginator, page)
            activities["updates"] = updates

    def handle_inserts(self, activities, limit, inserts_page):
        activities_insert = HistoricalActivity.objects.filter(fk_status_id=HistoricalActivity.STATUS_PENDING)
        activities_insert = self.apply_dashboard_filters(activities_insert)
        activities_insert = limit and activities_insert[:limit] or activities_insert
        paginator = Paginator(activities_insert, 10)
        page = _get_page(inserts_page, paginator)
        activities_insert = page.object_list
        inserts = {"cs": []}
        for cs in activities_insert:
            inserts["cs"].append(self.changeset_template_data(cs))
        if inserts["cs"]:
            inserts["pagination"] = _pagination_to_json(paginator, page)
            activities["inserts"] = inserts

    def handle_deletes(self, activities, limit, deletions_page):
        activities_deletes = HistoricalActivity.objects.filter(fk_status_id=HistoricalActivity.STATUS_TO_DELETE)
        activities_deletes = limit and activities_deletes[:limit] or activities_deletes
        paginator = Paginator(activities_deletes, 10)
        page = _get_page(deletions_page, paginator)
        activities_deletes = page.object_list
        deletes = {"cs": []}
        for cs in activities_deletes:
            comment = cs.comment and len(cs.comment) > 0 and cs.comment or "-"
            deletes["cs"].append({
                "id": cs.id,
                "deal_id": cs.fk_activity.activity_identifier,
                "user": cs.fk_user.username,
                "comment": comment
            })
        if deletes["cs"]:
            deletes["pagination"] = _pagination_to_json(paginator, page)
            activities["deletes"] = deletes

def _approve_investor_changes(investor, changeset):
    _update_investor_status(
        investor,
        Status.objects.get(name="overwritten" if changeset.previous_version else "active")
    )


def _reject_investor_changes(investor):
    _update_investor_status(investor, Status.objects.get(name="rejected"))


def _update_investor_status(investor, status):
    if not investor:
        return
    investor.fk_status = status
    investor.save()


def get_activity_investor(activity):
    iai = InvestorActivityInvolvement.objects.filter(fk_activity=activity).first()
    if iai:
        return Investor.objects.filter(id=iai.fk_investor).first()
    return None


def _uniquify_changesets_dict(changesets):
    unique, deals = [], []
    for cs in changesets.get('inserts', {}).get('cs', []):
        if cs['deal_id'] not in deals:
            unique.append(cs)
            deals.append(cs['deal_id'])
    changesets.get('inserts', {})['cs'] = unique
    unique = []
    for cs in changesets.get('updates', {}).get('cs', []):
        if cs['deal_id'] not in deals:
            unique.append(cs)
            deals.append(cs['deal_id'])
    changesets.get('updates', {})['cs'] = unique


def _uniquify_activities_by_deal(activities):
    unique, deals = [], []
    for activity in activities:
        if activity.activity_identifier not in deals:
            unique.append(activity)
            deals.append(activity.activity_identifier)
    return unique


def _filter_changesets_by_countries(activities, countries):
    return activities.filter(
        attributes__name='target_country',
        attributes__value__in=countries
    )


#def changeset_comment(changeset):
#    if changeset is None:
#        return 'changeset is None'
#
#    changeset = ActivityChangeset.objects.filter(id=changeset.id)
#    if len(changeset) > 0:
#        return changeset[0].comment
#    else:
#        return changeset.comment and len(changeset.comment) > 0 and changeset.comment or "-"


def _find_changed_fields(changeset):
    """
    This code never worked in the original Landmatrix. It is disabled until it is needed.
    """
    fields_changed = []
    return fields_changed

    activity = changeset.fk_activity
    prev_activity = activity.history.as_of(changeset.timestamp)
    prev_tags = dict(a.ActivityAttribute.history.filter(fk_activity=prev_activity). \
        filter(history_date__lte=changeset.timestamp).values_list('name', 'value'))
    tags = dict(ActivityAttribute.objects.filter(fk_activity=changeset.fk_activity) \
        .values_list('name', 'value'))

    prev_keys = []
    for key, value in tags.items():
        if key in prev_tags and value != prev_tags[key]:
            # field has been changed
            fields_changed.append(key)
            break
    for key in set(tags.keys()).difference(prev_tags.keys()):
        # field has been added or deleted
        fields_changed.append(key)
    return fields_changed


def _feedbacks_to_json(user, feedbacks_page=1, limit=None):
    feedbacks = []
    feed = ActivityFeedback.objects.get_current_feedbacks(user.id)
    feed = limit and feed[:limit] or feed
    paginator = Paginator(feed, 10)
    page = _get_page(feedbacks_page, paginator)
    feed = page.object_list
    for feedback in feed:
        feedbacks.append({
            "deal_id": feedback.fk_activity.activity_identifier,
            "from_user": feedback.fk_user_created.username,
            "comment": feedback.comment,
            "timestamp": feedback.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        })
    return {
        "feeds": feedbacks,
        "pagination": _pagination_to_json(paginator, page),
    }


def _rejected_to_json(user, limit=None):
    rejected = HistoricalActivity.objects.filter(fk_status__name='rejected', history_user_id=user.id)
    feed = limit and rejected[:limit] or rejected
    paginator = Paginator(feed, 10)
    page = _get_page(1, paginator)
    feed = page.object_list
    rejected = [
        {
            "deal_id": activity.activity_identifier,
            "user": user.username,
            "comment": _get_comment(activity),
            "timestamp": activity.history_date.strftime("%Y-%m-%d %H:%M:%S")
         } for activity in feed
    ]
    return {
        "cs": rejected,
        "pagination": _pagination_to_json(paginator, page),
    }


def _get_comment(historical_activity):
    changeset = ActivityChangeset.objects.filter(
        timestamp__gt=historical_activity.history_date - timedelta(seconds=1)
    ).filter(
        timestamp__lt=historical_activity.history_date + timedelta(seconds=1)
    ).filter(
        fk_activity_changeset__fk_activity_id=historical_activity.id
    ).first()
    return changeset.comment if changeset else None


def _get_page(page_number, paginator):
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page = paginator.page(paginator.num_pages)
    return page


def _pagination_to_json(paginator, page):
    pagination = {}
    if page.has_previous():
        pagination["previous"] = page.previous_page_number()
    if page.has_next():
        pagination["next"] = page.next_page_number()
    pagination["current"] = page.number
    pagination["last"] = paginator.num_pages
    pagination["total"] = paginator.count
    return pagination


def _approve_activity_change(activity, changeset, comment, request):
    _change_status_with_review(
        activity, Status.objects.get(name="overwritten" if changeset.previous_version else "active"),
        changeset, request.user,
        ReviewDecision.objects.get(name="approved"), comment
    )
    involvements = InvestorActivityInvolvement.objects.get_involvements_for_activity(activity)
    ap = ActivityProtocol()
    if len(involvements) > 0:
        _conditionally_update_stakeholders(activity, ap, involvements, request)
    # FIXME
    # Problem here: Involvements are not historical yet, but activity and investors are.
    # As an intermediate solution another involvement is created for each historical activity
    # which links to the public activity. Let's confirm the new and remove the old involvement.
    ap.prepare_deal_for_public_interface(activity.activity_identifier)


def _reject_activity_change(activity, changeset, comment, request):
    _change_status_with_review(
        activity, Status.objects.get(name="rejected"),
        changeset, request.user,
        ReviewDecision.objects.get(name="rejected"), comment
    )
    # FIXME
    # Problem here: Involvements are not historical yet, but activity and investors are.
    # As an intermediate solution another involvement is created for each historical activity
    # which links to the public activity. Let's remove the new involvement.


def _change_status_with_review(activity, status, changeset, user, review_decision, comment):
    activity.fk_status = status
    activity.save()
    ActivityChangeset.objects.create(
        fk_activity=activity,
        fk_user=user,
        fk_review_decision=review_decision,
        comment=comment
    )


def _conditionally_update_stakeholders(activity, ap, involvements, request):
    operational_stakeholder = involvements[0].fk_investor
    if _any_investor_has_changed(operational_stakeholder, involvements):
        # TODO make sure this is correct: secondary investors changed
        involvement_stakeholders = [
            {"stakeholder": ivi.fk_stakeholder, "investment_ratio": ivi.investment_ratio}
            for iai in involvements
            for ivi in InvestorVentureInvolvement.objects.filter(fk_investor=iai.fk_investor)
        ]

        ap.update_secondary_investors(
            activity, operational_stakeholder, involvement_stakeholders, request
        )


def _approve_activity_deletion(activity, changeset, cs_comment, request):
    activity.fk_status = Status.objects.get(name="deleted")
    activity.save()
    review_decision = ReviewDecision.objects.get(name="deleted")
    ActivityChangeset.objects.create(
        fk_activity=activity,
        fk_user=request.user,
        fk_review_decision=review_decision,
        comment=cs_comment
    )
    ActivityProtocol().remove_from_lookup_table(activity.activity_identifier)


def _any_investor_has_changed(operational_stakeholder, involvements):
    op_subinvestor_ids = set(s.investor_identifier for s in operational_stakeholder.subinvestors.all())
    involvement_investor_ids = (i.fk_investor.investor_identifier for i in involvements)
    return any(op_subinvestor_ids.symmetric_difference(involvement_investor_ids))

