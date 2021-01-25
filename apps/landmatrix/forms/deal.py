from apps.landmatrix.forms import VueForm
from apps.landmatrix.models import Deal, Crop, Animal, Mineral


class DealForm(VueForm):
    model = Deal

    @property
    def attributes(self):
        return {
            "intended_size": {"unit": "ha"},
            "contract_size": {"class": "JSONDateAreaField"},
            "production_size": {"class": "JSONDateAreaField"},
            "intention_of_investment": {
                "class": "JSONDateAreaChoicesField",
                "with_categories": True,
            },
            "negotiation_status": {
                "class": "JSONDateChoiceField",
                "choices": {
                    "EXPRESSION_OF_INTEREST": "Intended (Expression of interest)",
                    "UNDER_NEGOTIATION": "Intended (Under negotiation)",
                    "MEMORANDUM_OF_UNDERSTANDING": "Intended (Memorandum of understanding)",
                    "ORAL_AGREEMENT": "Concluded (Oral Agreement)",
                    "CONTRACT_SIGNED": "Concluded (Contract signed)",
                    "NEGOTIATIONS_FAILED": "Failed (Negotiations failed)",
                    "CONTRACT_CANCELED": "Failed (Contract cancelled)",
                    "CONTRACT_EXPIRED": "Contract expired",
                    "CHANGE_OF_OWNERSHIP": "Change of ownership",
                },
            },
            "implementation_status": {"class": "JSONDateChoiceField"},
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
            "involved_actors": {"class": "JSONActorsField"},
            "crops": {
                "class": "JSONExportsField",
                "choices": {c.code: c.name for c in Crop.objects.all()},
            },
            "animals": {
                "class": "JSONExportsField",
                "choices": {c.code: c.name for c in Animal.objects.all()},
            },
            "resources": {
                "class": "JSONExportsField",
                "choices": {c.code: c.name for c in Mineral.objects.all()},
            },
            "contract_farming_crops": {
                "class": "JSONDateAreaChoicesField",
                "choices": {c.code: c.name for c in Crop.objects.all()},
                "with_categories": False,
            },
            "contract_farming_animals": {
                "class": "JSONDateAreaChoicesField",
                "choices": {c.code: c.name for c in Animal.objects.all()},
                "with_categories": False,
            },
        }
