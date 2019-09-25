from django import forms
from django.utils.translation import ugettext_lazy as _

from apps.grid.fields import NestedMultipleChoiceField, TitleField
from apps.grid.widgets import CommentInput
from .base_form import BaseForm


class DealWaterForm(BaseForm):
    BOOLEAN_CHOICES = (("Yes", _("Yes")), ("No", _("No")))
    SOURCE_OF_WATER_EXTRACTION_CHOICES = (
        ("Groundwater", _("Groundwater"), None),
        (
            "Surface water",
            _("Surface water"),
            (("River", _("River")), ("Lake", _("Lake"))),
        ),
    )
    form_title = _("Water")

    tg_water_extraction_envisaged = TitleField(
        required=False, initial=_("Water extraction envisaged")
    )
    water_extraction_envisaged = forms.ChoiceField(
        required=False,
        label=_("Water extraction envisaged"),
        choices=BOOLEAN_CHOICES,
        widget=forms.RadioSelect,
    )
    tg_water_extraction_envisaged_comment = forms.CharField(
        required=False,
        label=_("Comment on water extraction envisaged"),
        widget=CommentInput,
    )

    tg_source_of_water_extraction = TitleField(
        required=False, initial=_("Source of water extraction")
    )
    source_of_water_extraction = NestedMultipleChoiceField(
        required=False,
        label=_("Source of water extraction"),
        choices=SOURCE_OF_WATER_EXTRACTION_CHOICES,
    )
    tg_source_of_water_extraction_comment = forms.CharField(
        required=False,
        label=_("Comment on source of water extraction"),
        widget=CommentInput,
    )

    tg_how_much_do_investors_pay = TitleField(
        required=False,
        initial=_(
            "How much do investors pay for water and the use of water infrastructure?"
        ),
    )
    tg_how_much_do_investors_pay_comment = forms.CharField(
        required=False,
        label=_("Comment on how much do investors pay for water"),
        widget=CommentInput,
    )

    tg_water_extraction_amount = TitleField(
        required=False, initial=_("How much water is extracted?")
    )
    water_extraction_amount = forms.CharField(
        required=False, label=_("Water extraction amount"), help_text=_("m3/year")
    )
    tg_water_extraction_amount_comment = forms.CharField(
        required=False,
        label=_("Comment on how much water is extracted"),
        widget=CommentInput,
    )

    use_of_irrigation_infrastructure = forms.ChoiceField(
        required=False,
        label=_("Use of irrigation infrastructure"),
        choices=BOOLEAN_CHOICES,
        widget=forms.RadioSelect,
    )
    tg_use_of_irrigation_infrastructure_comment = forms.CharField(
        required=False,
        label=_("Comment on use of irrigation infrastructure"),
        widget=CommentInput,
    )

    water_footprint = forms.CharField(
        required=False,
        label=_("Water footprint of the investment project"),
        widget=CommentInput,
    )

    class Meta:
        name = "water"
