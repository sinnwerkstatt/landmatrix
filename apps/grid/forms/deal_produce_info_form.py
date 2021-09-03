from django import forms
from django.utils.translation import gettext_lazy as _

from apps.grid.fields import TitleField, YearBasedModelMultipleChoiceIntegerField
from apps.grid.widgets import CommentInput, NumberInput
from apps.landmatrix.models import Animal, Country, Crop, Mineral
from .base_form import BaseForm


class DealProduceInfoForm(BaseForm):
    BOOLEAN_CHOICES = (("Yes", _("Yes")), ("No", _("No")))
    form_title = _("Produce info")

    # Detailed crop, animal and mineral information
    tg_crop_animal_mineral = TitleField(
        required=False,
        label="",
        initial=_("Detailed crop, animal and mineral information"),
    )
    crops = YearBasedModelMultipleChoiceIntegerField(
        required=False,
        label=_("Crops area"),
        queryset=Crop.objects.all(),
        placeholder=_("ha"),
    )
    crops_yield = YearBasedModelMultipleChoiceIntegerField(
        required=False,
        label=_("Crops yield"),
        queryset=Crop.objects.all(),
        placeholder=_("tons"),
    )
    crops_export = YearBasedModelMultipleChoiceIntegerField(
        required=False,
        label=_("Crops export"),
        queryset=Crop.objects.all(),
        placeholder=_("%"),
    )
    tg_crops_comment = forms.CharField(
        required=False, label=_("Comment on crops"), widget=CommentInput
    )
    animals = YearBasedModelMultipleChoiceIntegerField(
        required=False,
        label=_("Livestock area"),
        queryset=Animal.objects.all(),
        placeholder=_("ha"),
    )
    animals_yield = YearBasedModelMultipleChoiceIntegerField(
        required=False,
        label=_("Livestock yield"),
        queryset=Animal.objects.all(),
        placeholder=_("tons"),
    )
    animals_export = YearBasedModelMultipleChoiceIntegerField(
        required=False,
        label=_("Livestock export"),
        queryset=Animal.objects.all(),
        placeholder=_("%"),
    )
    tg_animals_comment = forms.CharField(
        required=False, label=_("Comment on livestock"), widget=CommentInput
    )
    minerals = YearBasedModelMultipleChoiceIntegerField(
        required=False,
        label=_("Resources area"),
        queryset=Mineral.objects.all(),
        placeholder=_("ha"),
    )
    minerals_yield = YearBasedModelMultipleChoiceIntegerField(
        required=False,
        label=_("Resources yield"),
        queryset=Mineral.objects.all(),
        placeholder=_("tons"),
    )
    minerals_export = YearBasedModelMultipleChoiceIntegerField(
        required=False,
        label=_("Resources export"),
        queryset=Mineral.objects.all(),
        placeholder=_("%"),
    )
    tg_minerals_comment = forms.CharField(
        required=False, label=_("Comment on resources"), widget=CommentInput
    )

    # Detailed contract farming crop and animal information
    tg_contract_farming_crop_animal_mineral = TitleField(
        required=False,
        initial=_("Detailed contract farming crop and animal information"),
    )
    contract_farming_crops = YearBasedModelMultipleChoiceIntegerField(
        required=False, label=_("Contract farming crops"), queryset=Crop.objects.all()
    )
    tg_contract_farming_crops_comment = forms.CharField(
        required=False,
        label=_("Comment on contract farming crops"),
        widget=CommentInput,
    )

    contract_farming_animals = YearBasedModelMultipleChoiceIntegerField(
        required=False,
        label=_("Contract farming livestock"),
        queryset=Animal.objects.all(),
    )
    tg_contract_farming_animals_comment = forms.CharField(
        required=False,
        label=_("Comment on contract farming livestock"),
        widget=CommentInput,
    )

    # Use of produce
    tg_use_of_produce = TitleField(
        required=False, label="", initial=_("Use of produce")
    )
    has_domestic_use = forms.BooleanField(required=False, label=_("Has domestic use"))
    domestic_use = forms.IntegerField(
        required=False, label=_("Domestic use"), help_text=_("%"), widget=NumberInput
    )
    has_export = forms.BooleanField(required=False, label=_("Has export"))
    export = forms.IntegerField(
        required=False, label=_("Export"), help_text=_("%"), widget=NumberInput
    )
    # TODO: surely this should be a formset?
    export_country1 = forms.ModelChoiceField(
        required=False,
        label=_("Country 1"),
        queryset=Country.objects.defer("geom").all().order_by("name"),
    )
    export_country1_ratio = forms.IntegerField(
        required=False, label=_("Country 1 ratio"), help_text=_("%"), widget=NumberInput
    )
    export_country2 = forms.ModelChoiceField(
        required=False,
        label=_("Country 2"),
        queryset=Country.objects.defer("geom").all().order_by("name"),
    )
    export_country2_ratio = forms.IntegerField(
        required=False, label=_("Country 2 ratio"), help_text=_("%"), widget=NumberInput
    )
    export_country3 = forms.ModelChoiceField(
        required=False,
        label=_("Country 3"),
        queryset=Country.objects.defer("geom").all().order_by("name"),
    )
    export_country3_ratio = forms.IntegerField(
        required=False, label=_("Country 3 ratio"), help_text=_("%"), widget=NumberInput
    )
    tg_use_of_produce_comment = forms.CharField(
        required=False, label=_("Comment on use of produce"), widget=CommentInput
    )

    # In-country processing of produce
    tg_in_country_processing = TitleField(
        required=False, label="", initial=_("In country processing of produce")
    )
    # TODO: YesNoField?
    in_country_processing = forms.ChoiceField(
        required=False,
        label=_("In country processing of produce"),
        choices=BOOLEAN_CHOICES,
        widget=forms.RadioSelect,
    )
    tg_in_country_processing_comment = forms.CharField(
        required=False,
        label=_("Comment on in country processing of produce"),
        widget=CommentInput,
    )
    processing_facilities = forms.CharField(
        required=False,
        label=_(
            "Processing facilities / production infrastructure of the project (e.g. oil mill, "
            "ethanol distillery, biomass power plant etc.)"
        ),
        widget=CommentInput,
    )
    in_country_end_products = forms.CharField(
        required=False,
        label=_("In-country end products of the project"),
        widget=CommentInput,
    )

    class Meta:
        name = "produce_info"


class PublicViewDealProduceInfoForm(DealProduceInfoForm):
    class Meta:
        name = "produce_info"
        fields = ("tg_crop_animal_mineral", "crops")
        readonly_fields = ("tg_crop_animal_mineral", "crops")
