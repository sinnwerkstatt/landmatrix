__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from .base_form import BaseForm
from grid.widgets import CommentInput, TitleField, PrimaryInvestorField

from django import forms
from django.utils.translation import ugettext_lazy as _


class DealPrimaryInvestorForm(BaseForm):
    tg_primary_investor = TitleField(required=False, label="", initial=_("Primary investor"))
    project_name = forms.CharField(required=False, label=_("Name of the investment project"), max_length=255)
    # TODO fix
    #primary_investor = forms.ChoiceField(required=False, label=_("Existing primary investor"), choices=PrimaryInvestor.objects._get_all_active_primary_investors_choices(), widget=PrimaryInvestorSelect)
    primary_investor = PrimaryInvestorField(required=False, label=_("Existing primary investor"))
    tg_primary_investor_comment = forms.CharField(required=False, label=_("Additional comments regarding investors"), widget=CommentInput)

    def __init__(self, *args, **kwargs):
        super(DealPrimaryInvestorForm, self).__init__(*args, **kwargs)
        self.fields["primary_investor"].choices = [("", str(_("---------"))),] + self.fields["primary_investor"].get_choices()


    def get_primary_investor(self):
        primary_investor = {
            "op": "add"
        }
        for j, taggroup in enumerate(super(DealPrimaryInvestorForm, self).get_attributes()):
            # Existing primary investor?
            for t in taggroup["tags"]:
                if t["key"] == "primary_investor" and t["value"]:
                    primary_investor["op"] = "select"
                    primary_investor["id"] = t["value"]
                if t["key"] == "primary_investor_name":
                    primary_investor["name"] = t["value"]
        return primary_investor

    def get_attributes(self, request=None):
        taggroups = super(DealPrimaryInvestorForm, self).get_attributes()
        for tg in taggroups:
            tags = []
            for t in tg["tags"]:
                if t["key"] == "project_name":
                    tags.append(t)
            tg["tags"] = tags
        return taggroups

    @classmethod
    def get_data(cls, activity):
        data = super(DealPrimaryInvestorForm, cls).get_data(activity)
        primary_investor = PrimaryInvestor.objects.get_primary_investor_for_activity(activity)
        if primary_investor:
            data["primary_investor"] = primary_investor.primary_investor_identifier
        return data

    def get_availability(self):
        """
        Availability of investor form is 1 if a primary investor is defined
        """
        if self.data.get("primary_investor", None) or self.data.get("primary_investor_name", None):
            return 1
        return 0

    def get_availability_total(self):
        return 1

    def clean_primary_investor(self):
        pi_id = None
        if self.data.get("primary_investor"):
            pi_id = int(self.data.get("primary_investor", 0))
        choices = dict(self.fields["primary_investor"].choices).keys()
        if pi_id and pi_id not in choices:
            #self.fields["primary_investor"].choices.append([pi_id, pi_name])
            #c_old = self.fields["primary_investor"].choices
            #self.base_fields["primary_investor"].choices.append([pi_id, pi_name])
            choices = self.fields["primary_investor"].get_choices()
            self.fields["primary_investor"].choices = choices
            self.base_fields["primary_investor"].choices = choices
            #self.base_fields["primary_investor"].update_choices()

            #c_new = self.fields["primary_investor"].choices
        return self.cleaned_data
