from django.contrib.postgres.forms import SimpleArrayField
from django.forms import (
    ModelForm,
    fields,
    ModelChoiceField,
    TypedChoiceField,
)
from django.utils.translation import gettext as _, gettext

from apps.landmatrix.forms import VueForm
from apps.landmatrix.forms.fields import (
    JSONDateAreaChoicesField,
    JSONDateAreaField,
    JSONDateChoiceField,
    JSONActorsField,
    JSONExportsField,
    JSONLeaseField,
    JSONJobsField,
)
from apps.landmatrix.models import Deal, Crop, Animal, Mineral
from apps.landmatrix.models._choices import (
    INTENTION_CHOICES,
    NEGOTIATION_STATUS_CHOICES,
    IMPLEMENTATION_STATUS_CHOICES,
    ACTOR_MAP,
)


class JSONFormOutputMixin:
    def as_json(self):
        ret = {}
        for name, field in self.fields.items():
            assert isinstance(field, fields.Field)
            field_json = {
                "label": field.label,
                "class": field.__class__.__name__,
                "required": field.required,
            }
            if field.help_text:
                field_json["help_text"] = gettext(field.help_text)
            if hasattr(field, "max_length") and field.max_length:
                field_json["max_length"] = field.max_length

            if isinstance(field, TypedChoiceField):
                field_json["choices"] = {x[0]: x[1] for x in field.choices}
            # if isinstance(field, IntegerField):
            #     breakpoint()
            # "min_value": field.min_value,
            # "max_value": field.max_value,
            # field_json["choices"] = {x[0]: x[1] for x in field.choices}
            if isinstance(field, ModelChoiceField):
                field_json["related_model"] = field.queryset.model.__name__
            if isinstance(field, SimpleArrayField):
                if hasattr(field.base_field, "choices"):
                    field_json["choices"] = {
                        x[0]: x[1] for x in field.base_field.choices
                    }
            if isinstance(
                field,
                (
                    JSONDateAreaChoicesField,
                    JSONDateChoiceField,
                    JSONActorsField,
                    JSONExportsField,
                ),
            ):
                field_json["choices"] = {x[0]: x[1] for x in field.choices}

            # if name == "domestic_use":
            #     breakpoint()

            if name in list(self.attributes.keys()):
                field_json.update(self.attributes[name])

            ret[name] = field_json

        return ret


class DealForm(JSONFormOutputMixin, ModelForm):
    contract_size = JSONDateAreaField(
        required=False,
        label=_("Size under contract (leased or purchased area, in ha)"),
        help_text=_("ha"),
    )
    production_size = JSONDateAreaField(
        required=False,
        label=_("Size in operation (production, in ha)"),
        help_text=_("ha"),
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
        label=_("Crops area/yield/export"),
        required=False,
    )
    animals = JSONExportsField(
        label=_("Livestock area/yield/export"),
        required=False,
    )
    mineral_resources = JSONExportsField(
        label=_("Mineral resources area/yield/export"),
        required=False,
    )
    contract_farming_crops = JSONDateAreaChoicesField(
        label=_("Contract farming crops"),
        help_text=_("ha"),
        required=False,
    )
    contract_farming_animals = JSONDateAreaChoicesField(
        label=_("Contract farming livestock"),
        help_text=_("ha"),
        required=False,
    )

    class Meta:
        model = Deal
        exclude = [
            "is_public",
            "has_known_investor",
            "not_public_reason",
            "parent_companies",
            "top_investors",
            "current_contract_size",
            "current_production_size",
            # "current_intention_of_investment",
            "current_negotiation_status",
            "current_implementation_status",
            "current_crops",
            "current_animals",
            "current_mineral_resources",
            "deal_size",
            "initiation_year",
            "forest_concession",
            "transnational",
            "geojson",
            "created_at",
            "created_by",
            "modified_at",
            "modified_by",
            "fully_updated_at",
            "status",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # print(self.fields["contract_size"])
        # print(self.fields["production_size"])
        # breakpoint()
        self.fields["operating_company"].choices = []
        crops_choices = [(x.code, x.name) for x in Crop.objects.all()]
        animals_choices = [(x.code, x.name) for x in Animal.objects.all()]
        self.fields["crops"].choices = crops_choices
        self.fields["animals"].choices = animals_choices
        self.fields["mineral_resources"].choices = [
            (x.code, x.name) for x in Mineral.objects.all()
        ]
        self.fields["contract_farming_crops"].choices = crops_choices
        self.fields["contract_farming_animals"].choices = animals_choices

    @property
    def attributes(self):
        return {
            "country": {"class": "CountryForeignKey"},
            "operating_company": {"class": "InvestorForeignKey"},
            "deal_size": {"unit": "ha"},
            "intended_size": {"unit": "ha"},
            "domestic_use": {"unit": "%", "min_value": 0, "max_value": 100},
            "export": {"unit": "%", "min_value": 0, "max_value": 100},
            "export_country1_ratio": {"unit": "%", "min_value": 0, "max_value": 100},
            "export_country2_ratio": {"unit": "%", "min_value": 0, "max_value": 100},
            "export_country3_ratio": {"unit": "%", "min_value": 0, "max_value": 100},
        }


class DealFrontendForm(VueForm):
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
                "choices": {x[0]: x[1] for x in INTENTION_CHOICES},
            },
            "negotiation_status": {
                "class": "JSONDateChoiceField",
                "choices": {x[0]: x[1] for x in NEGOTIATION_STATUS_CHOICES},
            },
            "implementation_status": {
                "class": "JSONDateChoiceField",
                "choices": {x[0]: x[1] for x in IMPLEMENTATION_STATUS_CHOICES},
            },
            "on_the_lease": {"class": "JSONLeaseField"},
            "off_the_lease": {"class": "JSONLeaseField"},
            "total_jobs_current": {"class": "JSONJobsField"},
            "foreign_jobs_current": {"class": "JSONJobsField"},
            "domestic_jobs_current": {"class": "JSONJobsField"},
            "involved_actors": {
                "class": "JSONActorsField",
                "choices": {x[0]: x[1] for x in ACTOR_MAP},
            },
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
                "help_text": _("ha"),
            },
            "contract_farming_animals": {
                "class": "JSONDateAreaChoicesField",
                "choices": {c.code: c.name for c in Animal.objects.all()},
                "with_categories": False,
                "help_text": _("ha"),
            },
            "export_country1": {"class": "CountryForeignKey"},
            "export_country2": {"class": "CountryForeignKey"},
            "export_country3": {"class": "CountryForeignKey"},
        }
