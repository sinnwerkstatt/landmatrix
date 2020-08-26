from apps.landmatrix.forms import VueForm
from apps.landmatrix.models import Investor, InvestorVentureInvolvement


class InvestorForm(VueForm):
    model = Investor


class InvestorVentureInvolvementForm(VueForm):
    model = InvestorVentureInvolvement
    attributes = {
        "involvement_type": {"class": "TextField", "label": "Involvement type"}
    }