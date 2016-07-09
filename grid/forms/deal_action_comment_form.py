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
        groups__name__in=("Editors", "Administrators")).order_by(
        "username")

    form_title = _('Action Comment')
    tg_action = TitleField(
        required=False, label="", initial=_("Action comment"))
    tg_action_comment = forms.CharField(
        required=True, label=_('Action comment'), widget=CommentInput)
    fully_updated = forms.BooleanField(
        required=False, label=_("Fully updated"))
    #fully_updated_history = forms.CharField(
    #    required=False, label=_("Fully updated history"),
    #    widget=forms.Textarea(attrs={"readonly":True, "cols": 80, "rows": 5}))


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

    class Meta:
        name = 'action_comment'
