from apps.landmatrix.forms import VueForm
from apps.landmatrix.models import Deal, Crop, Animal, Mineral
from django.utils.translation import gettext as _


class DealForm(VueForm):
    model = Deal
    extra_display_fields = {
        "workflowinfos": {
            "class": "WorkflowInfosField",
            "label": _("Comments / History"),
        },
        "combined_status": {"class": "StatusField"},
    }

    @property
    def attributes(self):
        return {
            "country": {"class": "CountryForeignKey"},
            "operating_company": {"class": "InvestorForeignKey"},
            "deal_size": {"unit": "ha"},
            "intended_size": {"unit": "ha"},
            "export": {"unit": "%"},
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
            "on_the_lease": {"class": "JSONLeaseField"},
            "off_the_lease": {"class": "JSONLeaseField"},
            "total_jobs_current": {"class": "JSONJobsField"},
            "foreign_jobs_current": {"class": "JSONJobsField"},
            "domestic_jobs_current": {"class": "JSONJobsField"},
            "involved_actors": {"class": "JSONActorsField"},
            "crops": {
                "class": "JSONExportsField",
                "choices": {c.code: c.name for c in Crop.objects.all()},
            },
            "animals": {
                "class": "JSONExportsField",
                "choices": {c.code: c.name for c in Animal.objects.all()},
            },
            "mineral_resources": {
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
            "export_country1": {"class": "CountryForeignKey"},
            "export_country2": {"class": "CountryForeignKey"},
            "export_country3": {"class": "CountryForeignKey"},
        }
