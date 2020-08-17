from apps.landmatrix.forms import VueForm
from apps.landmatrix.models import Deal, Crop, Animal, Mineral


class DealForm(VueForm):
    model = Deal

    @property
    def attributes(self):
        return {
            "crops": {"choices": {c.code: c.name for c in Crop.objects.all()}},
            "animals": {"choices": {c.code: c.name for c in Animal.objects.all()}},
            "resources": {"choices": {c.code: c.name for c in Mineral.objects.all()}},
            "intention_of_investment": {
                # multiselect: {
                #     multiple: true,
                #     with_categories: true,
                # },
            },
            "negotiation_status": {
                # multiselect: {
                #     multiple: false,
                # },
            },
            "implementation_status": {
                # multiselect: {
                #     multiple: false,
                # },
            },
        }
