__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from .base_form import BaseForm
from global_app.widgets import TitleField, CommentInput

from django import forms
from django.utils.translation import ugettext_lazy as _


class AddDealOverallCommentForm(BaseForm):

    form_title = _('Overall Comment')

    # Coordinators and reviewers overall comments
    tg_overall = TitleField(required=False, label="", initial=_("Overall comment"))
    tg_overall_comment = forms.CharField(required=False, label="", widget=CommentInput)
