from apps.landmatrix.forms import VueForm
from apps.landmatrix.models import Deal, Crop, Animal, Mineral


class DealForm(VueForm):
    model = Deal

    @property
    def attributes(self):
        return {
            "contract_size": {"jsondings": ["date", "size(ha)"]},
            "production_size": {"jsondings": ["date", "size(ha)"]},
            "intention_of_investment": {"jsondings": ["date", "size(ha)", "choice"]},
            "negotiation_status": {"jsondings": ["date", "choice"]},
            "implementation_status": {"jsondings": ["date", "choice"]},
            "on_the_lease": {"jsondings": ["date", "area", "farmers", "households"]},
            "off_the_lease": {"jsondings": ["date", "area", "farmers", "households"]},
            "total_jobs_current": {
                "jsondings": ["date", "jobs", "employees", "workers"]
            },
            "foreign_jobs_current": {
                "jsondings": ["date", "jobs", "employees", "workers"]
            },
            "domestic_jobs_current": {
                "jsondings": ["date", "jobs", "employees", "workers"]
            },
            "involved_actors": {"jsondings": ["value", "role"], "is_current": False},
            "crops": {
                "choices": {c.code: c.name for c in Crop.objects.all()},
                "jsondings": ["date", "choice", "area", "yield", "export"],
            },
            "animals": {
                "choices": {c.code: c.name for c in Animal.objects.all()},
                "jsondings": ["date", "choice", "area", "yield", "export"],
            },
            "resources": {
                "choices": {c.code: c.name for c in Mineral.objects.all()},
                "jsondings": ["date", "choice", "area", "yield", "export"],
            },
            "contract_farming_crops": {
                "choices": {c.code: c.name for c in Crop.objects.all()},
                "jsondings": ["date", "choice", "area"],
            },
            "contract_farming_animals": {
                "choices": {c.code: c.name for c in Crop.objects.all()},
                "jsondings": ["date", "choice", "area"],
            },
        }
