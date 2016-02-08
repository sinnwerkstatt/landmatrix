
from django.utils.encoding import force_text

from landmatrix.models.activity_changeset_review import ActivityChangesetReview
from landmatrix.models.activity_feedback import ActivityFeedback
from landmatrix.models.activity_changeset import ActivityChangeset

from django.views.generic import View
from django.http.response import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import json

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class ChangesetProtocol(View):

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
            return self.dashboard(request)
        else:
            raise IOError("Unknown action")

    def dashboard(self, request):
        from pprint import pprint
        res = {
            "latest_added": self.get_paged_results(
                ActivityChangeset.objects.get_by_state("active"), request.GET.get('latest_added_page')
            ),
            "latest_modified": self.get_paged_results(
                ActivityChangeset.objects.get_by_state("overwritten"), request.GET.get('latest_modified_page')
            ),
            "latest_deleted": self.get_paged_results(
                ActivityChangeset.objects.get_by_state("deleted"), request.GET.get('latest_deleted_page')
            ),
            "manage": self._changeset_to_json(limit=2),
            "feedbacks": self._feedbacks_to_json(request.user, limit=5)
        }
        pprint(res, width=150)
        return HttpResponse(json.dumps(res), content_type="application/json")

    def get_paged_results(self, records, page_number, per_page=10):
        paginator = Paginator(records, per_page)
        page = self._get_page(page_number, paginator)

        results = {"cs": []}
        for changeset in page.object_list:
            results["cs"].append(self.changeset_template_data(changeset))
        results["pagination"] = self._pagination_to_json(paginator, page)
        return results

    def changeset_template_data(self, changeset, extra_data=None):
        template_data = {
            "deal_id": 0 if not changeset or not changeset.fk_activity else changeset.fk_activity.activity_identifier,
            "user": force_text(_("Public User")) if not changeset or not changeset.fk_user else force_text(changeset.fk_user.username),
            "timestamp": 0 if not changeset else changeset.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "comment": self.changeset_comment(changeset)
        }
        if extra_data:
            template_data.update(extra_data)

        return template_data

    def changeset_comment(self, changeset):
        if changeset is None:
            return 'changeset is None'

        review = ActivityChangesetReview.objects.filter(fk_activity_changeset_id=changeset.id)
        if len(review) > 0:
            return review[0].comment
        else:
            return changeset.comment and len(changeset.comment) > 0 and changeset.comment or "-"

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
        changesets = {}
        if "my_deals" in self.data["a_changesets"]:
            self.handle_my_deals(changesets, ActivityChangeset.objects, limit, my_deals_page, user)
        if "updates" in self.data["a_changesets"]:
            self.handle_updates(changesets, ActivityChangeset.objects, limit, updates_page)
        if "inserts" in self.data["a_changesets"]:
            self.handle_inserts(changesets, ActivityChangeset.objects, inserts_page, limit)
        if "deletes" in self.data["a_changesets"]:
            self.handle_deletes(changesets, ActivityChangeset.objects, deletions_page, limit)
        if changesets:
            res["a_changesets"] = changesets

    def handle_my_deals(self, a_changesets, changesets, limit, my_deals_page, user):
        changesets_my_deals = changesets.get_my_deals(user.id)
        changesets_my_deals = limit and changesets_my_deals[:limit] or changesets_my_deals
        print('handle_my_deals', changesets_my_deals)
        paginator = Paginator(changesets_my_deals, 10)
        page = self._get_page(my_deals_page, paginator)
        changesets_my_deals = page.object_list
        my_deals = {"cs": []}
        for changeset in changesets_my_deals:
            my_deals["cs"].append(self.changeset_template_data(changeset, {"status": changeset.fk_activity.fk_status.name}))
        if my_deals["cs"]:
            my_deals["pagination"] = self._pagination_to_json(paginator, page)
            a_changesets["my_deals"] = my_deals

    def handle_updates(self, a_changesets, changesets, limit, updates_page):
        changesets_update = changesets.filter(fk_status__name="pending")  # , previous_version__isnull=False
        print(changesets.all())
        changesets_update = limit and changesets_update[:limit] or changesets_update
        print('handle_updates', changesets_update)
        paginator = Paginator(changesets_update, 10)
        page = self._get_page(updates_page, paginator)
        changesets_update = page.object_list
        updates = {"cs": []}
        for changeset in changesets_update:
            # find out which fields changed
            fields_changed = []
            # prev_activity = Activity.objects.get(activity_identifier=changeset.fk_activity.activity_identifier,
            #                                      version=changeset.previous_version)
            # prev_tags = A_Tag.objects.filter(fk_a_tag_group__fk_activity=prev_activity)
            # tags = A_Tag.objects.filter(fk_a_tag_group__fk_activity=changeset.fk_activity)
            # prev_keys = []
            # for tag in tags:
            #     for prev_tag in tags:
            #         if tag.fk_a_key.key == prev_tag.fk_a_key.key:
            #             if tag.fk_a_value != prev_tag.fk_a_value:
            #                 # field has been changed
            #                 fields_changed.append(tag.fk_a_key.id)
            #             break
            # for key in set([t.fk_a_key.id for t in tags]).difference([t.fk_a_key.id for t in prev_tags]):
            #     # field has been added or deleted
            #     fields_changed.append(key)
            # comment = changeset.comment and len(changeset.comment) > 0 and changeset.comment or "-"
            updates["cs"].append(self.changeset_template_data(changeset, {"fields_changed": fields_changed}))
        if updates["cs"]:
            updates["pagination"] = self._pagination_to_json(paginator, page)
            a_changesets["updates"] = updates

    def handle_inserts(self, a_changesets, changesets, inserts_page, limit):
        changesets_insert = changesets.filter(fk_status__name="pending")  #  previous_version__isnull=True)
        changesets_insert = limit and changesets_insert[:limit] or changesets_insert
        paginator = Paginator(changesets_insert, 10)
        page = self._get_page(inserts_page, paginator)
        changesets_insert = page.object_list
        inserts = {"cs": []}
        for cs in changesets_insert:
            inserts["cs"].append(self.changeset_template_data(cs))
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

