__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from grid.widgets import TitleField, CommentInput

from .base_form import BaseForm

from django import forms
from django.utils.translation import ugettext_lazy as _


class ManageDealForm(BaseForm):

    tg_action = TitleField(required=False, label="", initial=_("Action comment"))
    tg_action_comment = forms.CharField(required=False, label="", widget=CommentInput)

    def __init__(self, *args, **kwargs):
        if "instance" in kwargs:
            kwargs.pop("instance")
        super(ManageDealForm, self).__init__(*args, **kwargs)

    def save(self):
        return self
