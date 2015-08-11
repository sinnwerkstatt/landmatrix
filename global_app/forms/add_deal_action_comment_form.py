__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from .base_form import BaseForm
from global_app.widgets import TitleField, CommentInput, UserModelChoiceField
from landmatrix.models.activity import Activity

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.dateformat import DateFormat
from django.contrib.auth.models import User

class AddDealActionCommentForm(BaseForm):
    tg_action = TitleField(required=False, label="", initial=_("Action comment"))
    tg_action_comment = forms.CharField(required=False, label="", widget=CommentInput)
    fully_updated = forms.BooleanField(required=False, label=_("Fully updated"))
    fully_updated_history = forms.CharField(required=False, label=_("Fully updated history"), widget=forms.Textarea(attrs={"readonly":True, "cols": 80, "rows": 5}))


    tg_not_public = TitleField(required=False, label="", initial=_("Public deal"))
    not_public = forms.BooleanField(required=False, label=_("Not public"), help_text=_("Please specify in additional comment field"))
    not_public_reason = forms.ChoiceField(required=False, label=_("Reason"), choices=(
        (0, _("---------")),
        (10, _("Temporary removal from PI after criticism")),
        (20, _("Research in progress")),
    ))
    tg_not_public_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)

    tg_feedback = TitleField(required=False, label="", initial=_("Feedback"))
    assign_to_user = UserModelChoiceField(required=False, label=_("Assign to"), queryset=User.objects.filter(groups__name__in=("Research admins", "Research assistants")).order_by("username"), empty_label=_("Unassigned"))
    tg_feedback_comment = forms.CharField(required=False, label=_("Feedback comment"), widget=CommentInput)

    def get_action_comment(self):
        for j, taggroup in enumerate(super(AddDealActionCommentForm, self).get_taggroups()):
            if taggroup["main_tag"]["value"] == "action":
                return taggroup["comment"]
        return ""

    def get_feedback(self):
        for j, taggroup in enumerate(super(AddDealActionCommentForm, self).get_taggroups()):
            if taggroup["main_tag"]["value"] == "feedback":
                tags = taggroup.get("tags", [])
                if len(tags) > 0:
                    feedback = {
                        "assigned_to": tags[0].get("value"),
                        "comment": taggroup.get("comment")
                    }
                    return feedback
        return ""

    def get_fully_updated(self):
        for j, taggroup in enumerate(super(AddDealActionCommentForm, self).get_taggroups()):
            if taggroup["main_tag"]["value"] == "action":
                for tag in taggroup.get("tags", []):
                    if tag.get("key") == "fully_updated":
                        return tag.get("value")
        return False

    def get_taggroups(self, request=None):
        taggroups = []
        for tg in super(AddDealActionCommentForm, self).get_taggroups():
            if tg["main_tag"]["value"] in ("action", "feedback"):
                continue
            else:
                taggroups.append(tg)
        return taggroups

    @classmethod
    def get_data(cls, activity):
        data = super(AddDealActionCommentForm, cls).get_data(activity)
        a_feedback = A_Feedback.objects.filter(fk_activity=activity)
        if len(a_feedback) > 0:
            feedback = a_feedback[0]
            data.update({
                "assign_to_user": feedback.fk_user_assigned.id,
                "tg_feedback_comment": feedback.comment,
            })
        fully_updated_history = Activity.objects.get_fully_updated_history(activity.activity_identifier)
        fully_updated = []
        for h in fully_updated_history:
            fully_updated.append("%s - %s: %s" %(DateFormat(h.fully_updated).format("Y-m-d H:i:s"), h.username, h.comment))
        data.update({
            "fully_updated_history": "\n".join(fully_updated)
        })
        return data
