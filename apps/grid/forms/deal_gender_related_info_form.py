from django import forms
from django.utils.translation import ugettext_lazy as _

from apps.grid.fields import TitleField
from apps.grid.widgets import CommentInput
from .base_form import BaseForm


class DealGenderRelatedInfoForm(BaseForm):

    form_title = _('Gender-related info')

    tg_gender_specific_info = TitleField(
        required=False, label="",
        initial=_("Any gender-specific information about the investment and its impacts"))
    tg_gender_specific_info_comment = forms.CharField(
        required=False, label=_("Comment on gender-related info"),
        widget=CommentInput)

    class Meta:
        name = 'gender-related_info'
