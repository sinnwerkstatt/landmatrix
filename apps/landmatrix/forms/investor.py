from django.utils.translation import ugettext as _

from apps.landmatrix.forms import VueForm
from apps.landmatrix.models import Investor


class InvestorForm(VueForm):
    model = Investor
    sections = {
        "general_info": {
            "label": _("Investor"),
            "fields": [
                "name",
                "country",
                "classification",
                "homepage",
                "opencorporates",
                "comment",
            ],
        }
    }
