from inspect import currentframe, getframeinfo

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.dateformat import DateFormat
from django.contrib.auth import get_user_model

from landmatrix.models.activity import Activity
from grid.widgets import TitleField, CommentInput, UserModelChoiceField
from .base_form import BaseForm


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'
User = get_user_model()


class DealActionCommentForm(BaseForm):
    NOT_PUBLIC_REASON_CHOICES = (
        ("---------", _("---------")),
        (
            "Temporary removal from PI after criticism",
            _("Temporary removal from PI after criticism"),
        ),
        ("Research in progress", _("Research in progress")),
        ('Land Observatory Import (new)', _('Land Observatory Import (new)')),
        (
            'Land Observatory Import (duplicate)',
            _('Land Observatory Import (duplicate)'),
        ),
    )
    ASSIGN_TO_USER_QUERYSET = User.objects.filter(
        groups__name__in=("Research admins", "Research assistants")).order_by(
        "username")

    form_title = _('Action Comment')
    tg_action = TitleField(
        required=False, label="", initial=_("Action comment"))
    tg_action_comment = forms.CharField(
        required=True, label="", widget=CommentInput)
    fully_updated = forms.BooleanField(
        required=False, label=_("Fully updated"))
    fully_updated_history = forms.CharField(
        required=False, label=_("Fully updated history"),
        widget=forms.Textarea(attrs={"readonly":True, "cols": 80, "rows": 5}))


    tg_not_public = TitleField(
        required=False, label="", initial=_("Public deal"))
    not_public = forms.BooleanField(
        required=False, label=_("Not public"),
        help_text=_("Please specify in additional comment field"))
    not_public_reason = forms.ChoiceField(
        required=False, label=_("Reason"), choices=NOT_PUBLIC_REASON_CHOICES)
    tg_not_public_comment = forms.CharField(
        required=False, label=_("Public deal comments"), widget=CommentInput)

    tg_feedback = TitleField(required=False, label="", initial=_("Feedback"))
    assign_to_user = UserModelChoiceField(
        required=False, label=_("Assign to"), queryset=ASSIGN_TO_USER_QUERYSET,
        empty_label=_("Unassigned"))
    tg_feedback_comment = forms.CharField(
        required=False, label=_("Feedback comment"), widget=CommentInput)

    def get_action_comment(self):
        for j, group in enumerate(super().get_attributes()):
            if group["main_tag"]["value"] == "action":
                return group["comment"]
        return ""

    def get_feedback(self):
        for j, group in enumerate(super().get_attributes()):
            if group["main_tag"]["value"] == "feedback":
                tags = group.get("tags", [])
                if len(tags) > 0:
                    feedback = {
                        "assigned_to": tags[0].get("value"),
                        "comment": group.get("comment")
                    }
                    return feedback
        return ""

    def get_fully_updated(self):
        for j, group in enumerate(super().get_attributes()):
            if group["main_tag"]["value"] == "action":
                for tag in group.get("tags", []):
                    if tag.get("key") == "fully_updated":
                        return tag.get("value")
        return False

    @classmethod
    def get_data(cls, activity, group=None, prefix=None):
        '''
        TODO: this getframeinfo stuff is bad.
        '''
        data = super().get_data(activity)
        if False:
            # TODO: NameError here (A_Feedback)
            a_feedback = A_Feedback.objects.filter(fk_activity=activity)
        else:
            frameinfo = getframeinfo(currentframe())
            print(
                '*** feedback not yet implemented!', frameinfo.filename,
                frameinfo.lineno)
            a_feedback = []

        if len(a_feedback) > 0:
            feedback = a_feedback[0]
            data.update({
                "assign_to_user": feedback.fk_user_assigned.id,
                "tg_feedback_comment": feedback.comment,
            })
        if False:
            fully_updated_history = Activity.objects.get_fully_updated_history(
                activity.activity_identifier)
        else:
            frameinfo = getframeinfo(currentframe())
            print(
                '*** fully updated history not yet implemented!',
                frameinfo.filename, frameinfo.lineno)
            fully_updated_history = []

        fully_updated = []
        for h in fully_updated_history:
            fully_updated.append(
                "%s - %s: %s" % (
                    DateFormat(h.fully_updated).format("Y-m-d H:i:s"),
                    h.username, h.comment
                ))
        data.update({
            "fully_updated_history": "\n".join(fully_updated)
        })
        return data

    class Meta:
        name = 'action_comment'