from apps.landmatrix.forms import VueForm
from apps.landmatrix.models import Investor, InvestorVentureInvolvement
from django.utils.translation import gettext as _


class InvestorForm(VueForm):
    model = Investor
    extra_display_fields = {
        "deals": {"class": "LengthField", "label": _("Deals")},
        "workflowinfos": {
            "class": "WorkflowInfosField",
            "label": _("Comments / History"),
        },
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
