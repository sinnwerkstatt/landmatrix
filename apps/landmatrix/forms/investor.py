from django.forms import ModelForm, IntegerField
from django.utils.translation import gettext as _

from apps.landmatrix.forms.formfieldhelper import JSONFormOutputMixin
from apps.landmatrix.models import Investor, InvestorVentureInvolvement


class InvestorForm(JSONFormOutputMixin, ModelForm):
    class Meta:
        model = Investor
        exclude = [
            "involvements",
            "investors",
            "current_draft",
            "old_id",
            "is_actually_unknown",
            "status",
            "created_at",
        ]

    attributes = {"country": {"class": "CountryForeignKey"}}
    extra_display_fields = {
        "id": {"label": "ID", "class": "AutoField"},
        "deals": {"class": "LengthField", "label": _("Deals")},
        "workflowinfos": {
            "class": "WorkflowInfosField",
            "label": _("Comments / History"),
        },
        "combined_status": {"class": "StatusField"},
    }


class InvestorVentureInvolvementForm(JSONFormOutputMixin, ModelForm):
    class Meta:
        model = InvestorVentureInvolvement
        fields = "__all__"

    attributes = {
        "involvement_type": {"class": "TextField", "label": _("Involvement type")},
        "investor": {"class": "InvestorForeignKey"},
        "venture": {"class": "InvestorForeignKey"},
        "percentage": {"unit": "%", "min_value": 0, "max_value": 100},
        "loans_date": {"class": "DateField"},
    }
