from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.template.context import RequestContext
from django.conf import settings
from django.utils.datastructures import MultiValueDict
from django.views.generic import TemplateView
from math import ceil

from global_app.views.view_aux_functions import render_to_response
from landmatrix.models.activity import Activity
from landmatrix.models.activity_attribute_group import ActivityAttributeGroup
from landmatrix.models.activity_feedback import ActivityFeedback
from landmatrix.models.language import Language
from landmatrix.models.activity_changeset import ActivityChangeset

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class EditorView(TemplateView):

    template_name = 'dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return self.render_authenticated_user(request)
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    def render_authenticated_user(self, request):
        csp = ChangesetProtocol()
        data = {
            "a_changesets":["updates", "deletes", "inserts"],
            "sh_changesets": ["deletes"],
        }
        request.POST = MultiValueDict({"data": [json.dumps(data)]})
        response = csp.dispatch(request, action="dashboard")
        response = json.loads(response.content.decode())
        data = {
            "statistics": {
                "overall_deal_count": get_overall_deal_count(),
                "public_deal_count": get_public_deal_count(),
                "deals_changed_count": get_deal_changed_count_since_import(),
                "deals_added_count": get_deal_added_count_since_import(),
            },
            "view": "dashboard",
            "latest_added": response["latest_added"],
            "latest_modified": response["latest_modified"],
            "latest_deleted": response["latest_deleted"],
            "manage": response["manage"],
            "feedbacks": response["feedbacks"],
        }
        return render_to_response(self.template_name, data, RequestContext(request))
        context = {
            'user': request.user,
            'latest_modified': self.latest_modified(),
            'latest_added': self.latest_added(),
            'latest_deleted': self.latest_deleted(),
            'attention_needed': self.attention_needed(request.user),
            'feedback_requests': self.feedback_requests(request.user)
        }
        return render_to_response(self.template_name, context, RequestContext(request))

    def latest_modified(self):
        
        return []

    def latest_added(self):
        return []

    def latest_deleted(self):
        return []

    def attention_needed(self, user):
        return []

    def feedback_requests(self, user):
        return []


def get_overall_deal_count():
    return Activity.objects.filter(fk_status__name__in=('active', 'overwritten')).values('activity_identifier').count()


from django.db import connection


def get_public_deal_count():
    cursor = connection.cursor()

    cursor.execute("""
SELECT COUNT(DISTINCT a.activity_identifier) AS count
FROM landmatrix_activity AS a
JOIN landmatrix_status AS st ON a.fk_status_id = st.id
LEFT JOIN landmatrix_activityattributegroup AS a5 ON a.id = a5.fk_activity_id AND a5.attributes ? 'production_size'
LEFT JOIN landmatrix_activityattributegroup AS a4 ON a.id = a4.fk_activity_id AND a4.attributes ? 'contract_size'
LEFT JOIN landmatrix_activityattributegroup AS a6 ON a.id = a6.fk_activity_id AND a6.attributes ? 'intended_size'
LEFT JOIN landmatrix_activityattributegroup AS a3 ON a.id = a3.fk_activity_id AND a3.attributes ? 'not_public'
LEFT JOIN landmatrix_activityattributegroup AS a2 ON a.id = a2.fk_activity_id AND a2.attributes ? 'negotiation_status'
LEFT JOIN landmatrix_activityattributegroup AS a1 ON a.id = a1.fk_activity_id AND a1.attributes ? 'implementation_status'
WHERE a.fk_status_id = st.id
AND st.name IN ('active', 'overwritten')
AND (CAST(a5.attributes->'production_size' AS NUMERIC) >= 200 OR (a5.attributes->'production_size') IS NULL)
AND (CAST(a4.attributes->'contract_size' AS NUMERIC) >= 200 OR (a4.attributes->'contract_size') IS NULL)
AND ((a4.attributes->'contract_size') IS NULL
    AND ((a5.attributes->'production_size') IS NULL)
    AND CAST(a6.attributes->'intended_size' AS NUMERIC) >= 200 OR (a6.attributes->'intended_size') IS NULL
)
AND (a3.attributes->'not_public' NOT IN ('True', 'on') OR (a3.attributes->'not_public') IS NULL)
AND (
    a2.attributes->'negotiation_status' IN ('Oral Agreement', 'Contract signed')
    AND a2.date >= '2000-01-01'
    OR (a2.attributes->'negotiation_status') IS NULL
)
AND (
    a1.attributes->'implementation_status' <> 'Project abandoned'
    OR (a1.attributes->'implementation_status') IS NULL
);
""")
    row = cursor.fetchone()
    return row[0] if row else 0


def get_deal_changed_count_since_import():
    return 0
    cursor = connection.cursor()

    cursor.execute("""
SELECT
                count(distinct a.id) as count
FROM
                activities a,
                status st
WHERE
                a.version = (SELECT max(version) FROM activities amax, status st WHERE amax.fk_status = st.id AND amax.activity_identifier = a.activity_identifier AND st.name IN ("active", "overwritten", "deleted"))
                AND a.fk_status = st.id
                AND st.name IN ("overwritten")
                AND a.activity_identifier <= %i
""" % MAX_IMPORT_DEAL_ID)
    row = cursor.fetchone()
    return row[0] if row else 0


def get_deal_added_count_since_import():
    return 0
    cursor = connection.cursor()

    cursor.execute("""
              SELECT
                count(distinct a.id) as count
              FROM
                activities a,
                status st
              WHERE
                a.version = (SELECT max(version) FROM activities amax, status st WHERE amax.fk_status = st.id AND amax.activity_identifier = a.activity_identifier AND st.name IN ("active", "overwritten", "deleted"))
                AND a.fk_status = st.id
                AND st.name IN ("active", "overwritten")
                AND a.activity_identifier > %i
        """ % MAX_IMPORT_DEAL_ID)
    row = cursor.fetchone()
    return row[0] if row else 0


import json
from django.views.generic import View


class Protocol(View):

    # LANG_DEFAULT = Language.objects._get_language("en")

    def _pagination_to_json(self, paginator, page):
        pagination = {}
        if page.has_previous():
            pagination["previous"] = page.previous_page_number()
        if page.has_next():
            pagination["next"] = page.next_page_number()
        pagination["current"] = page.number
        pagination["last"] = paginator.num_pages
        pagination["total"] = paginator.count
        return pagination

    def _get_page(self, page_number, paginator):
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            page = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            page = paginator.page(paginator.num_pages)
        return page

class ChangesetProtocol(Protocol):

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
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
            return ChangesetProtocol.dashboard(self, request, *args, **kwargs)
        else:
            raise IOError("Unknown action")

    def dashboard(self, request, *args, **kwargs):
        changesets = ActivityChangeset.objects
        hectares, country = "", ""
        res = {
                "latest_added": [],
                "latest_modified": [],
                "latest_deleted": [],
                "manage": []
                }
        # latest added
        res_latest_added = {"cs":[]}
        paginator = Paginator(changesets.get_by_state("active"), 10)
        page = self._get_page(request.GET.get('latest_added_page'), paginator)
        for cs in page.object_list:
            comment = ""
            review = A_Changeset_Review.objects.filter(fk_a_changeset=cs.id)
            if len(review) > 0:
                comment = review[0].comment
            else:
                comment = cs.comment and len(cs.comment) > 0 and cs.comment or "-"
            res_latest_added["cs"].append({
                "deal_id": cs.fk_activity.activity_identifier,
                "user": cs.fk_user and cs.fk_user.username or unicode(_("Public User")),
                "timestamp": cs.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "comment": comment
                })
        res_latest_added["pagination"] = self._pagination_to_json(paginator, page)
        res["latest_added"] = res_latest_added
        # latest modified
        res_latest_modified = {"cs":[]}
        paginator = Paginator(changesets.get_by_state("overwritten"), 10)
        page = self._get_page(request.GET.get('latest_modified_page'), paginator)
        for cs in page.object_list:
            comment = ""
            review = A_Changeset_Review.objects.filter(fk_a_changeset=cs.id)
            if len(review) > 0:
                comment = review[0].comment
            else:
                comment = cs.comment and len(cs.comment) > 0 and cs.comment or "-"
            res_latest_modified["cs"].append({
                "deal_id": cs.fk_activity.activity_identifier,
                "user": cs.fk_user and cs.fk_user.username or unicode(_("Public User")),
                "timestamp": cs.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "comment": comment
                })
        res_latest_modified["pagination"] = self._pagination_to_json(paginator, page)
        res["latest_modified"] = res_latest_modified
        # latest deleted
        res_latest_deleted = {"cs":[]}
        paginator = Paginator(changesets.get_by_state("deleted"), 10)
        page = self._get_page(request.GET.get('latest_deleted_page'), paginator)
        for cs in page.object_list:
            comment = ""
            review = A_Changeset_Review.objects.filter(fk_a_changeset=cs.id)
            if len(review) > 0:
                comment = review[0].comment
            else:
                comment = cs.comment and len(cs.comment) > 0 and cs.comment or "-"
            res_latest_deleted["cs"].append({
                "deal_id": cs.fk_activity.activity_identifier,
                "user": cs.fk_user and cs.fk_user.username or str(_("Public User")),
                "timestamp": cs.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "comment":comment
                })
        res_latest_deleted["pagination"] = self._pagination_to_json(paginator, page)
        res["latest_deleted"] = res_latest_deleted

        res["manage"] = self._changeset_to_json(limit=2)
        res["feedbacks"] = self._feedbacks_to_json(request.user, limit=5)
        return HttpResponse(json.dumps(res), content_type="application/json")

    def _changeset_to_json(self, user=None, my_deals_page=1, updates_page=1, inserts_page=1, deletions_page=1, limit=None):
        res = {}
        if not self.data:
            self.data = {
                "a_changesets": ["updates", "deletes", "inserts"],
                #"sh_changesets": ["deletes"],
            }
        if "a_changesets" in self.data:
            self.handle_a_changesets(deletions_page, inserts_page, limit, my_deals_page, res, updates_page, user)
        if "sh_changesets" in self.data:
            self.handle_sh_changesets(deletions_page, limit, res)
        return res

    def handle_a_changesets(self, deletions_page, inserts_page, limit, my_deals_page, res, updates_page, user):
        a_changesets = {}
        changesets = ActivityChangeset.objects
        if "my_deals" in self.data["a_changesets"]:
            self.handle_my_deals(a_changesets, changesets, limit, my_deals_page, user)
        if "updates" in self.data["a_changesets"]:
            self.handle_updates(a_changesets, changesets, limit, updates_page)
        if "inserts" in self.data["a_changesets"]:
            self.handle_inserts(a_changesets, changesets, inserts_page, limit)
        if "deletes" in self.data["a_changesets"]:
            self.handle_deletes(a_changesets, changesets, deletions_page, limit)
        if a_changesets:
            res["a_changesets"] = a_changesets

    def handle_updates(self, a_changesets, changesets, limit, updates_page):
        changesets_update = changesets.filter(fk_status__name="pending")  # , previous_version__isnull=False
        changesets_update = limit and changesets_update[:limit] or changesets_update
        paginator = Paginator(changesets_update, 10)
        page = self._get_page(updates_page, paginator)
        changesets_update = page.object_list
        updates = {"cs": []}
        for cs in changesets_update:
            # find out which fields changed
            fields_changed = []
            prev_activity = Activity.objects.get(activity_identifier=cs.fk_activity.activity_identifier,
                                                 version=cs.previous_version)
            prev_tags = A_Tag.objects.filter(fk_a_tag_group__fk_activity=prev_activity)
            tags = A_Tag.objects.filter(fk_a_tag_group__fk_activity=cs.fk_activity)
            prev_keys = []
            for tag in tags:
                for prev_tag in tags:
                    if tag.fk_a_key.key == prev_tag.fk_a_key.key:
                        if tag.fk_a_value != prev_tag.fk_a_value:
                            # field has been changed
                            fields_changed.append(tag.fk_a_key.id)
                        break
            for key in set([t.fk_a_key.id for t in tags]).difference([t.fk_a_key.id for t in prev_tags]):
                # field has been added or deleted
                fields_changed.append(key)
            comment = cs.comment and len(cs.comment) > 0 and cs.comment or "-"
            updates["cs"].append({
                "id": cs.id,
                "deal_id": cs.fk_activity.activity_identifier,
                "user": cs.fk_user and cs.fk_user.username or unicode(_("Public User")),
                "fields_changed": fields_changed,
                "comment": comment
            })
        if updates["cs"]:
            updates["pagination"] = self._pagination_to_json(paginator, page)
            a_changesets["updates"] = updates

    def handle_my_deals(self, a_changesets, changesets, limit, my_deals_page, user):
        changesets_my_deals = changesets.get_my_deals(user.id)
        changesets_my_deals = limit and changesets_my_deals[:limit] or changesets_my_deals
        paginator = Paginator(changesets_my_deals, 10)
        page = self._get_page(my_deals_page, paginator)
        changesets_my_deals = page.object_list
        my_deals = {"cs": []}
        for cs in changesets_my_deals:
            comment = ""
            review = A_Changeset_Review.objects.filter(fk_a_changeset=cs.id)
            if len(review) > 0:
                comment = review[0].comment
            else:
                comment = cs.comment and len(cs.comment) > 0 and cs.comment or "-"
            my_deals["cs"].append({
                "deal_id": cs.fk_activity.activity_identifier,
                "timestamp": cs.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "comment": comment,
                "status": cs.fk_activity.fk_status.name
            })
        if my_deals["cs"]:
            my_deals["pagination"] = self._pagination_to_json(paginator, page)
            a_changesets["my_deals"] = my_deals

    def handle_inserts(self, a_changesets, changesets, inserts_page, limit):
        changesets_insert = changesets.filter(fk_status__name="pending")  #  previous_version__isnull=True)
        changesets_insert = limit and changesets_insert[:limit] or changesets_insert
        paginator = Paginator(changesets_insert, 10)
        page = self._get_page(inserts_page, paginator)
        changesets_insert = page.object_list
        inserts = {"cs": []}
        for cs in changesets_insert:
            comment = cs.comment and len(cs.comment) > 0 and cs.comment or "-"
            inserts["cs"].append({
                "id": cs.id,
                "deal_id": cs.fk_activity.activity_identifier,
                "user": cs.fk_user and cs.fk_user.username or unicode(_("Public User")),
                "comment": comment
            })
        if inserts["cs"]:
            inserts["pagination"] = self._pagination_to_json(paginator, page)
            a_changesets["inserts"] = inserts

    def handle_deletes(self, a_changesets, changesets, deletions_page, limit):
        changesets_delete = changesets.filter(fk_status__name="to_delete")
        changesets_delete = limit and changesets_delete[:limit] or changesets_delete
        paginator = Paginator(changesets_delete, 10)
        page = self._get_page(deletions_page, paginator)
        changesets_delete = page.object_list
        deletes = {"cs": []}
        for cs in changesets_delete:
            comment = cs.comment and len(cs.comment) > 0 and cs.comment or "-"
            deletes["cs"].append({
                "id": cs.id,
                "deal_id": cs.fk_activity.activity_identifier,
                "user": cs.fk_user.username,
                "comment": comment
            })
        if deletes["cs"]:
            deletes["pagination"] = self._pagination_to_json(paginator, page)
            a_changesets["deletes"] = deletes

    def handle_sh_changesets(self, deletions_page, limit, res):
        print('SH changesets not yet implemented!')
        return
        sh_changesets = {}
        if "deletes" in self.data["sh_changesets"]:
            changesets_delete = SH_Changeset.objects.filter(fk_stakeholder__fk_status__name="to_delete").order_by(
                "-timestamp")
            changesets_delete = limit and changesets_delete[:limit] or changesets_delete
            paginator = Paginator(changesets_delete, 10)
            page = self._get_page(deletions_page, paginator)
            changesets_delete = page.object_list
            deletes = {"cs": []}
            for cs in changesets_delete:
                comment = cs.comment and len(cs.comment) > 0 and cs.comment or "-"
                deletes["cs"].append({
                    "id": cs.id,
                    "investor_id": cs.fk_stakeholder.stakeholder_identifier,
                    "user": cs.fk_user.username,
                    "comment": comment
                })
            if deletes["cs"]:
                deletes["pagination"] = self._pagination_to_json(paginator, page)
                sh_changesets["deletes"] = deletes
        if sh_changesets:
            res["sh_changesets"] = sh_changesets

    def _feedbacks_to_json(self, user, feedbacks_page=1, limit=None):
        feedbacks = []
        feed = ActivityFeedback.objects.get_current_feedbacks(user.id)
        feed = limit and feed[:limit] or feed
        paginator = Paginator(feed, 10)
        page = self._get_page(feedbacks_page, paginator)
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
            "pagination": self._pagination_to_json(paginator, page),
        }


class InvalidPage(Exception):
    pass


class PageNotAnInteger(InvalidPage):
    pass


class EmptyPage(InvalidPage):
    pass


class Paginator(object):

    def __init__(self, object_list, per_page, orphans=0,
                 allow_empty_first_page=True):
        self.object_list = object_list
        self.per_page = int(per_page)
        self.orphans = int(orphans)
        self.allow_empty_first_page = allow_empty_first_page
        self._num_pages = self._count = None

    def validate_number(self, number):
        """
        Validates the given 1-based page number.
        """
        try:
            number = int(number)
        except (TypeError, ValueError):
            raise PageNotAnInteger('That page number is not an integer')
        if number < 1:
            raise EmptyPage('That page number is less than 1')
        if number > self.num_pages:
            if number == 1 and self.allow_empty_first_page:
                pass
            else:
                raise EmptyPage('That page contains no results')
        return number

    def page(self, number):
        """
        Returns a Page object for the given 1-based page number.
        """
        number = self.validate_number(number)
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        if top + self.orphans >= self.count:
            top = self.count
        return self._get_page(self.object_list[bottom:top], number, self)

    def _get_page(self, *args, **kwargs):
        """
        Returns an instance of a single page.

        This hook can be used by subclasses to use an alternative to the
        standard :cls:`Page` object.
        """
        return Page(*args, **kwargs)

    def _get_count(self):
        """
        Returns the total number of objects, across all pages.
        """
        if self._count is None:
            try:
                self._count = self.object_list.count()
            except (AttributeError, TypeError):
                # AttributeError if object_list has no count() method.
                # TypeError if object_list.count() requires arguments
                # (i.e. is of type list).
                self._count = len(self.object_list)
        return self._count
    count = property(_get_count)

    def _get_num_pages(self):
        """
        Returns the total number of pages.
        """
        if self._num_pages is None:
            if self.count == 0 and not self.allow_empty_first_page:
                self._num_pages = 0
            else:
                hits = max(1, self.count - self.orphans)
                self._num_pages = int(ceil(hits / float(self.per_page)))
        return self._num_pages
    num_pages = property(_get_num_pages)

    def _get_page_range(self):
        """
        Returns a 1-based range of pages for iterating through within
        a template for loop.
        """
        return list(six.moves.range(1, self.num_pages + 1))
    page_range = property(_get_page_range)


from collections import Sequence


class Page(Sequence):

    def __init__(self, object_list, number, paginator):
        self.object_list = object_list
        self.number = number
        self.paginator = paginator

    def __repr__(self):
        return '<Page %s of %s>' % (self.number, self.paginator.num_pages)

    def __len__(self):
        return len(self.object_list)

    def __getitem__(self, index):
        if not isinstance(index, (slice,) + six.integer_types):
            raise TypeError
        # The object_list is converted to a list so that if it was a QuerySet
        # it won't be a database hit per __getitem__.
        if not isinstance(self.object_list, list):
            self.object_list = list(self.object_list)
        return self.object_list[index]

    def has_next(self):
        return self.number < self.paginator.num_pages

    def has_previous(self):
        return self.number > 1

    def has_other_pages(self):
        return self.has_previous() or self.has_next()

    def next_page_number(self):
        return self.paginator.validate_number(self.number + 1)

    def previous_page_number(self):
        return self.paginator.validate_number(self.number - 1)

    def start_index(self):
        """
        Returns the 1-based index of the first object on this page,
        relative to total objects in the paginator.
        """
        # Special case, return zero if no items.
        if self.paginator.count == 0:
            return 0
        return (self.paginator.per_page * (self.number - 1)) + 1

    def end_index(self):
        """
        Returns the 1-based index of the last object on this page,
        relative to total objects found (hits).
        """
        # Special case for the last page because there can be orphans.
        if self.number == self.paginator.num_pages:
            return self.paginator.count
        return self.number * self.paginator.per_page
