from django.forms import ModelForm

from apps.landmatrix.forms import VueForm
from apps.landmatrix.models import Investor, InvestorVentureInvolvement
from django.utils.translation import gettext as _


class InvestorForm(ModelForm):
    class Meta:
        model = Investor
        exclude = [
            "involvements",
            "current_draft",
            "created_at",
            "created_by",
            "modified_at",
            "modified_by",
            "old_id",
            "is_actually_unknown",
        ]


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


class InvestorVentureInvolvementForm(VueForm):
    model = InvestorVentureInvolvement
    attributes = {
        "involvement_type": {"class": "TextField", "label": _("Involvement type")},
        "investor": {"class": "InvestorForeignKey"},
        "venture": {"class": "InvestorForeignKey"},
        "percentage": {"unit": "%"},
        "loans_date": {"class": "DateField"},
    }
