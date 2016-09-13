import json

from django.forms.fields import CharField
from django.forms.widgets import Textarea
from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView
from django.utils.datastructures import MultiValueDict
from django.template.context import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from landmatrix.models.activity import HistoricalActivity
from landmatrix.models.investor import HistoricalInvestor
from editor.views.changeset_protocol import ChangesetProtocol
from grid.forms.base_form import BaseForm
from grid.views.view_aux_functions import render_to_response
from grid.widgets.title_field import TitleField


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class ManageView(TemplateView):

    template_name = 'manage.html'

    def get(self, request):
        csp = ChangesetProtocol()
        request.POST = MultiValueDict(
            {"data": [json.dumps(
                {"activities": ["updates", "deletes", "inserts", "rejected"],
                 "investors": ["deletes"]}
            )]}
        )
        response = csp.dispatch(request, action="list")
        response = json.loads(response.content.decode())
        data = {
            "view": "manage"
        }

        data.update(response.get("activities", {}))

        if "updates" in data:
            changed = []
            for activity in data["updates"]:
                for k in activity.get("fields_changed", []):
                    changed.append(str(get_field_by_a_key_id(k).label))
                activity["fields_changed"] = ", ".join(changed)

        data.update({"investors": response.get("investors", {}).get("deletes", {})})
        data.update({"feedbacks": response.get("feedbacks", [])})
        data.update({"rejected": response.get("rejected", [])})

        return render_to_response(
            self.template_name, data, context_instance=RequestContext(request))


class CommentInput(Textarea):
    def render(self, name, value, attrs=None):
        if not attrs:
            attrs = {}
        attrs.update({'rows': '3'})
        return super(CommentInput, self).render(name, value, attrs)


class ManageDealForm(BaseForm):
    tg_action = TitleField(required=False, label="", initial=_("Action comment"))
    tg_action_comment = CharField(required=False, label="", widget=CommentInput)

    def __init__(self, *args, **kwargs):
        kwargs.pop("instance", None)
        super().__init__(*args, **kwargs)

    def save(self):
        return self


class ManageContentView(UpdateView):
    template_name = "manage_item.html"
    form_class = ManageDealForm
    success_url = "/editor/manage/"
    instance = None

    def get_context_data(self, **kwargs):
        context = super(ManageContentView, self).get_context_data(**kwargs)
        context.update({
            "view": "manage_content_view",
            "id": self.item_id,
            "action": self.action,
            "type": self.type,
        })

        return context

    def get_object(self, queryset=None):
        self.type = self.kwargs['type']
        self.action = self.kwargs['action']
        self.id = self.kwargs['id']
        if self.type == "deal":
            self.instance = HistoricalActivity.objects.get(id=self.id)
            self.item_id = self.instance.activity_identifier
        else:
            self.instance = HistoricalInvestor.objects.get(id=self.id)
            self.item_id = self.instance.investor_identifier
        return self.instance

    def form_valid(self, form):
        comment = self.request.POST["tg_action_comment"]
        cp = ChangesetProtocol()
        if self.type == "deal":
            data = {
                "activities": [{"id": self.instance.id, "comment": comment}]
            }
        else:
            data = {
                "investors": [{"id": self.instance.id, "comment": comment}]
            }
        self.request.POST = MultiValueDict({"data": [json.dumps(data)]})
        response = cp.dispatch(self.request, action=self.action)
        response = json.loads(response.content.decode())
        if len(response["errors"]) > 0:
            for e in response["errors"]:
                messages.error(self.request, e)
        else:
            messages.success(self.request, "%s has been successfully %s" % (
                self.type == "deal" and "Deal" or "Investor",
                self.action == "approve" and "Approved" or "Rejected")
            )
        return super(ManageContentView, self).form_valid(form)
