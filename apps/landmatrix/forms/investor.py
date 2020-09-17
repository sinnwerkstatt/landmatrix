from apps.landmatrix.forms import VueForm
from apps.landmatrix.models import Investor, InvestorVentureInvolvement
from django.utils.translation import ugettext as _


class InvestorForm(VueForm):
    model = Investor


class InvestorVentureInvolvementForm(VueForm):
    model = InvestorVentureInvolvement
    attributes = {
        "involvement_type": {"class": "TextField", "label": _("Involvement type")}
    }
