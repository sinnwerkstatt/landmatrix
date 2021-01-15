from apps.landmatrix.forms import VueForm
from apps.landmatrix.models import Deal, Crop, Animal, Mineral


class DealForm(VueForm):
    model = Deal

    @property
    def attributes(self):
        return {
            "intended_size": {"unit": "ha"},
            "contract_size": {
                "class": "JSONDateAreaField",
                "dimensions": ["date", "area"],
            },
            "production_size": {
                "class": "JSONDateAreaField",
                "dimensions": ["date", "area"],
            },
            "intention_of_investment": {
                "class": "JSONDateAreaChoicesField",
                "dimensions": ["date", "choices", "area"],
                "multiselect": {"with_categories": True, "multiple": True},
            },
            "negotiation_status": {
                "class": "JSONDateChoiceField",
                "dimensions": ["date", "choice"],
            },
            "implementation_status": {
                "class": "JSONDateChoiceField",
                "dimensions": ["date", "choice"],
            },
            # "on_the_lease": {
            #     "class": "JSONLeaseField",
            #     "dimensions": ["date", "area", "farmers", "households"],
            # },
            # "off_the_lease": {
            #     "class": "JSONLeaseField",
            #     "dimensions": ["date", "area", "farmers", "households"],
            # },
            # "total_jobs_current": {
            #     "class": "JSONJobsField",
            #     "dimensions": ["date", "jobs", "employees", "workers"],
            # },
            # "foreign_jobs_current": {
            #     "class": "JSONJobsField",
            #     "dimensions": ["date", "jobs", "employees", "workers"],
            # },
            # "domestic_jobs_current": {
            #     "class": "JSONJobsField",
            #     "dimensions": ["date", "jobs", "employees", "workers"],
            # },
            "involved_actors": {
                "class": "JSONActorsField",
                "dimensions": ["name", "role"],
                "has_current": False,
            },
            "crops": {
                "class": "JSONExportsField",
                "choices": {c.code: c.name for c in Crop.objects.all()},
                "dimensions": ["date", "choices", "area", "yield", "export"],
            },
            "animals": {
                "class": "JSONExportsField",
                "choices": {c.code: c.name for c in Animal.objects.all()},
                "dimensions": ["date", "choices", "area", "yield", "export"],
            },
            "resources": {
                "class": "JSONExportsField",
                "choices": {c.code: c.name for c in Mineral.objects.all()},
                "dimensions": ["date", "choices", "area", "yield", "export"],
            },
            "contract_farming_crops": {
                "class": "JSONDateAreaChoicesField",
                "choices": {c.code: c.name for c in Crop.objects.all()},
                "dimensions": ["date", "choices", "area"],
            },
            "contract_farming_animals": {
                "class": "JSONDateAreaChoicesField",
                "choices": {c.code: c.name for c in Animal.objects.all()},
                "dimensions": ["date", "choices", "area"],
            },
        }
