from django.forms import ModelForm, IntegerField

from apps.landmatrix.forms import VueForm
from apps.landmatrix.forms.formfieldhelper import JSONFormOutputMixin
from apps.landmatrix.models import Investor, InvestorVentureInvolvement
from django.utils.translation import gettext as _


class InvestorForm(JSONFormOutputMixin, ModelForm):
    id = IntegerField(label=_("ID"))

    class Meta:
        model = Investor
        exclude = [
            "involvements",
            "current_draft",
            "old_id",
            "is_actually_unknown",
        ]

    attributes = {"country": {"class": "CountryForeignKey"}}


class InvestorFrontendForm(VueForm):
    model = Investor
    extra_display_fields = {
        "deals": {"class": "LengthField", "label": _("Deals")},
        "workflowinfos": {
            "class": "WorkflowInfosField",
            "label": _("Comments / History"),
        },
        "combined_status": {"class": "StatusField"},
    }
    attributes = {"country": {"class": "CountryForeignKey"}}


class InvestorVentureInvolvementForm(JSONFormOutputMixin, ModelForm):
    class Meta:
        model = InvestorVentureInvolvement
        fields = "__all__"

    attributes = {
        "involvement_type": {"class": "TextField", "label": _("Involvement type")},
        "investor": {"class": "InvestorForeignKey"},
        "venture": {"class": "InvestorForeignKey"},
        "percentage": {"unit": "%"},
        "loans_date": {"class": "DateField"},
    }


class InvestorVentureInvolvementFrontendForm(VueForm):
    model = InvestorVentureInvolvement
    attributes = {
        "involvement_type": {"class": "TextField", "label": _("Involvement type")},
        "investor": {"class": "InvestorForeignKey"},
        "venture": {"class": "InvestorForeignKey"},
        "percentage": {"unit": "%"},
        "loans_date": {"class": "DateField"},
    }
