from django import forms
from django.forms.models import ModelChoiceField
from django.utils.translation import gettext_lazy as _

from apps.grid.fields import ActorsField, TitleField
from apps.grid.forms.base_form import BaseForm
from apps.grid.forms.choices import actor_choices
from apps.grid.widgets import CommentInput, InvestorSelect
from apps.landmatrix.models.investor import HistoricalInvestor


# FIXME: Rename to OperatingCompanyForm
class OperationalStakeholderForm(BaseForm):
    exclude_in_export = ("operational_stakeholder",)

    form_title = _("Investor info")

    tg_operational_stakeholder = TitleField(
        required=False, label="", initial=_("Operating company")
    )
    operational_stakeholder = ModelChoiceField(
        required=False,
        label=_("Operating company"),
        queryset=HistoricalInvestor.objects.none(),
        widget=InvestorSelect(attrs={"class": "form-control investorfield"}),
    )
    actors = ActorsField(
        required=False,
        label=_("Actors involved in the negotiation / admission process"),
        choices=actor_choices,
    )
    project_name = forms.CharField(
        required=False, label=_("Name of investment project"), max_length=255
    )
    tg_operational_stakeholder_comment = forms.CharField(
        required=False, label=_("Comment on investment chain"), widget=CommentInput
    )

    @classmethod
    def get_data(cls, activity, group=None, prefix=""):
        data = super().get_data(activity, group, prefix)

        # Get operating company
        queryset = activity.involvements.order_by("-id")
        if queryset.count() > 0:
            data["operational_stakeholder"] = str(queryset[0].fk_investor.id)
        return data

    def clean_operational_stakeholder(self):
        # Check if investor ID is newest version ID
        # This is necessary e.g. if ES index is not up-to-date or investor changed during adding/editing deal
        hinv = self.cleaned_data["operational_stakeholder"]
        data = None
        if hinv:
            data = HistoricalInvestor.objects.filter(
                investor_identifier=hinv.investor_identifier
            ).latest()
        return data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Show given/current value only, rest happens via ajax
        valid_choice = self.data.get(
            "operational_stakeholder", self.initial.get("operational_stakeholder", None)
        )
        if valid_choice:
            field = self.fields["operational_stakeholder"]
            field.queryset = HistoricalInvestor.objects.filter(pk=valid_choice)
            # Add investor identifier as data attribute
            if field.queryset.count() > 0:
                field.widget.data = {
                    str(valid_choice): {
                        "investor-identifier": field.queryset[0].investor_identifier
                    }
                }

    class Meta:
        name = "investor_info"
