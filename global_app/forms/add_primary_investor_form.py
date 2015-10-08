__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from landmatrix.models.primary_investor import PrimaryInvestor

from .base_form import BaseForm
from global_app.widgets import CommentInput

from django import forms
from django.utils.translation import ugettext_lazy as _


class AddPrimaryInvestorForm(BaseForm):
    """
        used only in the add primary investor dialog and not in the wizard.
    """
    primary_investor_name = forms.CharField(required=True, label=_("Name of primary investor"), max_length=255)
    action_comment = forms.CharField(required=False, label=_("Action comment"), widget=CommentInput)

    def __init__(self, *args, **kwargs):
        if "instance" in kwargs:
            kwargs.pop("instance")
        super(AddPrimaryInvestorForm, self).__init__(*args, **kwargs)

    def clean_primary_investor_name(self):
        pi_name = self.cleaned_data["primary_investor_name"]
        pi = PrimaryInvestor.objects._get_active_primary_investor_by_name(pi_name)
        if pi_name and pi:
             raise forms.ValidationError(_("Primary investor name already exists. Please choose a different name."))
        return pi_name

    def save(self):
        return self
