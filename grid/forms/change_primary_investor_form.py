__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from .base_form import BaseForm
from grid.widgets import CommentInput

from django import forms
from django.utils.translation import ugettext_lazy as _


class ChangePrimaryInvestorForm(BaseForm):
    """
        used only in the change primary investor dialog and not in the wizard.
    """
    primary_investor_name = forms.CharField(required=True, label=_("Name of primary investor"), max_length=255)
    action_comment = forms.CharField(required=False, label=_("Action comment"), widget=CommentInput)

    def __init__(self, *args, **kwargs):
        if "instance" in kwargs:
            kwargs.pop("instance")
        super(ChangePrimaryInvestorForm, self).__init__(*args, **kwargs)

    def save(self):
        return self
