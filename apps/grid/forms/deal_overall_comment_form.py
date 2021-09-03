from django import forms
from django.utils.translation import gettext_lazy as _

from apps.grid.fields import TitleField
from apps.grid.widgets import CommentInput
from .base_form import BaseForm


class DealOverallCommentForm(BaseForm):
    form_title = _("Overall Comment")
    # Coordinators and reviewers overall comments
    tg_overall = TitleField(required=False, label="", initial=_("Overall comment"))
    tg_overall_comment = forms.CharField(
        required=False, label=_("Overall comment"), widget=CommentInput
    )

    class Meta:
        name = "overall_comment"
