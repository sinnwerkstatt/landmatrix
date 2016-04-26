
__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from .base_form import BaseForm

from grid.widgets import TitleField, CommentInput, NumberInput
from landmatrix.models.animal import Animal
from landmatrix.models.country import Country
from landmatrix.models.crop import Crop
from landmatrix.models.mineral import Mineral

from django import forms
from django.utils.translation import ugettext_lazy as _


class DealProduceInfoForm(BaseForm):

    form_title = _('Produce info')

    # Detailed crop, animal and mineral information
    tg_crop_animal_mineral = TitleField(
        required=False, label="", initial=_("Detailed crop, animal and mineral information")
    )
    crops = forms.ModelMultipleChoiceField(
        required=False, label=_("Crops"), queryset=Crop.objects.all()
    )
    crops_other = forms.CharField(
        required=False, label=_("Other crops")
    )
    tg_crops_comment = forms.CharField(
        required=False, label=_("Additional comments"), widget=CommentInput
    )
    animals = forms.ModelMultipleChoiceField(
        required=False, label=_("Livestock"), queryset=Animal.objects.all()
    )
    animals_other = forms.CharField(
        required=False, label=_("Other livestock")
    )
    tg_animals_comment = forms.CharField(
        required=False, label=_("Additional comments"), widget=CommentInput
    )
    minerals = forms.ModelMultipleChoiceField(
        required=False, label=_("Resources"), queryset=Mineral.objects.all()
    )
    minerals_other = forms.CharField(
        required=False, label=_("Other resources")
    )
    tg_minerals_comment = forms.CharField(
        required=False, label=_("Additional comments"), widget=CommentInput
    )
    contract_farming_crops = forms.ModelMultipleChoiceField(
        required=False, label=_("Contract farming crops"), queryset=Crop.objects.all()
    )
    contract_farming_crops_other = forms.CharField(
        required=False, label=_("Other contract farming crops")
    )

    # Detailed contract farming crop, animal and mineral information
    tg_contract_farming_crop_animal_mineral = TitleField(
        required=False, initial=_("Detailed contract farming crop, animal and mineral information")
    )
    tg_contract_farming_crops_comment = forms.CharField(
        required=False, label=_("Additional comments"), widget=CommentInput
    )
    contract_farming_animals = forms.ModelMultipleChoiceField(
        required=False, label=_("Contract farming livestock"), queryset=Animal.objects.all()
    )
    contract_farming_animals_other = forms.CharField(
        required=False, label=_("Other contract farming livestock")
    )
    tg_contract_farming_animals_comment = forms.CharField(
        required=False, label=_("Additional comments"), widget=CommentInput
    )

    # Use of produce
    tg_use_of_produce = TitleField(required=False, label="", initial=_("Use of produce"))
    has_domestic_use = forms.BooleanField(required=False, label=_("Has domestic use"))
    domestic_use = forms.IntegerField(required=False, label=_("Domestic use"), help_text=_("%"), widget=NumberInput)
    has_export = forms.BooleanField(required=False, label=_("Has export"))
    export = forms.IntegerField(required=False, label=_("Export"), help_text=_("%"), widget=NumberInput)
    export_country1 = forms.ModelChoiceField(required=False, label=_("Country 1"), queryset=Country.objects.all().order_by("name"))
    export_country1_ratio = forms.IntegerField(required=False, label=_("Country 1 ratio"), help_text=_("%"), widget=NumberInput)
    export_country2 = forms.ModelChoiceField(required=False, label=_("Country 2"), queryset=Country.objects.all().order_by("name"))
    export_country2_ratio = forms.IntegerField(required=False, label=_("Country 2 ratio"), help_text=_("%"), widget=NumberInput)
    export_country3 = forms.ModelChoiceField(required=False, label=_("Country 3"), queryset=Country.objects.all().order_by("name"))
    export_country3_ratio = forms.IntegerField(required=False, label=_("Country 3 ratio"), help_text=_("%"), widget=NumberInput)
    tg_use_of_produce_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)

    # In-country processing of produce
    tg_in_country_processing = TitleField(
        required=False, label="", initial=_("In country processing of produce")
    )
    in_country_processing = forms.ChoiceField(
        required=False, label=_("In country processing of produce"), choices=(
            (10, _("Yes")),
            (20, _("No")),
        ), widget=forms.RadioSelect
    )
    tg_in_country_processing_comment = forms.CharField(
        required=False, label=_("Additional comments"), widget=CommentInput
    )
    processing_facilities = forms.CharField(
        required=False,
        label=_("Processing facilities / production infrastructure of the project (e.g. oil mill, "
                "ethanol distillery, biomass power plant etc.)"),
        widget=CommentInput
    )

    class Meta:
        name = 'produce_info'


class PublicViewDealProduceInfoForm(DealProduceInfoForm):

    class Meta:
        name = 'produce_info'
        fields = (
            "tg_crop_animal_mineral", "crops",
        )
        readonly_fields = (
            "tg_crop_animal_mineral", "crops",
        )
