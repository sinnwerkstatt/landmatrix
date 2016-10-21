from django import forms
from django.utils.translation import ugettext_lazy as _

from grid.fields import TitleField
from grid.widgets import CommentInput
from .base_form import BaseForm


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class DealOverallCommentForm(BaseForm):
    form_title = _('Overall Comment')
    # Coordinators and reviewers overall comments
    tg_overall = TitleField(
        required=False, label="", initial=_("Overall comment"))
    tg_overall_comment = forms.CharField(
        required=False, label=_("Overall comment"), widget=CommentInput)

    class Meta:
        name = 'overall_comment'
