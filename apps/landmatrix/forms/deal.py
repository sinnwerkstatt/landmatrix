from django.forms import ModelForm
from django.utils.translation import gettext as _

from apps.landmatrix.forms.fields import (
    JSONDateAreaChoicesField,
    JSONDateAreaField,
    JSONDateChoiceField,
    JSONActorsField,
    JSONExportsField,
    JSONLeaseField,
    JSONJobsField,
)
from apps.landmatrix.forms.formfieldhelper import JSONFormOutputMixin
from apps.landmatrix.models.choices import (
    INTENTION_CHOICES,
    NEGOTIATION_STATUS_CHOICES,
    IMPLEMENTATION_STATUS_CHOICES,
    CROPS_CHOICES,
    ANIMALS_CHOICES,
    MINERALS_CHOICES,
)
from apps.landmatrix.models.deal import Deal


class DealForm(JSONFormOutputMixin, ModelForm):
    contract_size = JSONDateAreaField(
        required=False,
        label=_("Size under contract (leased or purchased area, in ha)"),
    )
    production_size = JSONDateAreaField(
        required=False,
        label=_("Size in operation (production, in ha)"),
    )
    intention_of_investment = JSONDateAreaChoicesField(
        required=False, label=_("Intention of investment"), choices=INTENTION_CHOICES
    )
    negotiation_status = JSONDateChoiceField(
        required=False,
        label=_("Negotiation status"),
        choices=NEGOTIATION_STATUS_CHOICES,
    )
    implementation_status = JSONDateChoiceField(
        required=False,
        label=_("Implementation status"),
        choices=IMPLEMENTATION_STATUS_CHOICES,
    )
    on_the_lease = JSONLeaseField(
        label=_("On leased area/farmers/households"),
        required=False,
    )
    off_the_lease = JSONLeaseField(
        label=_("Not on leased area/farmers/households (out-grower)"),
        required=False,
    )
    total_jobs_current = JSONJobsField(
        required=False,
        label=_("Current total number of jobs/employees/ daily/seasonal workers"),
    )
    foreign_jobs_current = JSONJobsField(
        required=False,
        label=_("Current foreign number of jobs/employees/ daily/seasonal workers"),
    )
    domestic_jobs_current = JSONJobsField(
        required=False,
        label=_("Current domestic number of jobs/employees/ daily/seasonal workers"),
    )
    involved_actors = JSONActorsField(
        label=_("Actors involved in the negotiation / admission process"),
        required=False,
    )
    crops = JSONExportsField(
        label=_("Crops area/yield/export"), required=False, choices=CROPS_CHOICES
    )
    animals = JSONExportsField(
        label=_("Livestock area/yield/export"), required=False, choices=ANIMALS_CHOICES
    )
    mineral_resources = JSONExportsField(
        label=_("Mineral resources area/yield/export"),
        required=False,
        choices=MINERALS_CHOICES,
    )
    contract_farming_crops = JSONDateAreaChoicesField(
        label=_("Contract farming crops"),
        help_text=_("ha"),
        required=False,
        choices=CROPS_CHOICES,
    )
    contract_farming_animals = JSONDateAreaChoicesField(
        label=_("Contract farming livestock"),
        help_text=_("ha"),
        required=False,
        choices=ANIMALS_CHOICES,
    )

    extra_display_fields = {
        "id": {"label": "ID", "class": "AutoField"},
        "workflowinfos": {
            "class": "WorkflowInfosField",
            "label": _("Comments / History"),
        },
        "combined_status": {"class": "StatusField"},
    }

    class Meta:
        model = Deal
        exclude = [
            "is_public",
            "has_known_investor",
            "not_public_reason",
            "parent_companies",
            "top_investors",
            # "current_contract_size",
            # "current_production_size",
            # "current_intention_of_investment",
            # "current_negotiation_status",
            # "current_implementation_status",
            # "current_crops",
            # "current_animals",
            # "current_mineral_resources",
            "initiation_year",
            "forest_concession",
            "transnational",
            "geojson",
            "status",
            "draft_status",
            "current_draft",
        ]

    @property
    def attributes(self):
        return {
            "country": {"class": "CountryForeignKey"},
            "operating_company": {"class": "InvestorForeignKey"},
            "deal_size": {"unit": _("ha")},
            "intended_size": {"unit": _("ha")},
            "purchase_price_currency": {"class": "CurrencyForeignKey"},
            "annual_leasing_fee_currency": {"class": "CurrencyForeignKey"},
            "total_jobs_planned": {"unit": _("jobs")},
            "total_jobs_planned_employees": {"unit": _("employees")},
            "total_jobs_planned_daily_workers": {"unit": _("workers")},
            "foreign_jobs_planned": {"unit": _("jobs")},
            "foreign_jobs_planned_employees": {"unit": _("employees")},
            "foreign_jobs_planned_daily_workers": {"unit": _("workers")},
            "domestic_jobs_planned": {"unit": _("jobs")},
            "domestic_jobs_planned_employees": {"unit": _("employees")},
            "domestic_jobs_planned_daily_workers": {"unit": _("workers")},
            "domestic_use": {"unit": "%", "min_value": 0, "max_value": 100},
            "export": {"unit": "%", "min_value": 0, "max_value": 100},
            "export_country1": {"class": "CountryForeignKey"},
            "export_country1_ratio": {"unit": "%", "min_value": 0, "max_value": 100},
            "export_country2": {"class": "CountryForeignKey"},
            "export_country2_ratio": {"unit": "%", "min_value": 0, "max_value": 100},
            "export_country3": {"class": "CountryForeignKey"},
            "export_country3_ratio": {"unit": "%", "min_value": 0, "max_value": 100},
            "water_extraction_amount": {"unit": _("m3/year")},
        }
