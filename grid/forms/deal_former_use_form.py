from django import forms
from django.utils.translation import ugettext_lazy as _

from grid.forms.base_form import BaseForm
from grid.fields import TitleField
from grid.widgets import CommentInput


class DealFormerUseForm(BaseForm):
    FORMER_LAND_OWNER_CHOICES = (
        ("State", _("State")),
        ("Private (smallholders)", _("Private (smallholders)")),
        ("Private (large-scale)", _("Private (large-scale farm)")),
        ("Community", _("Community")),
        ("Indigenous people", _("Indigenous people")),
        ("Other", _("Other")),
    )
    FORMER_LAND_USE_CHOICES = (
        ("Commercial (large-scale) agriculture", _("Commercial (large-scale) agriculture")),
        ("Smallholder agriculture", _("Smallholder agriculture")),
        ("Shifting cultivation", _("Shifting cultivation")),
        ("Pastoralism", _("Pastoralism")),
        ("Hunting/Gathering", _("Hunting/Gathering")),
        ("Forestry", _("Forestry")),
        ("Conservation", _("Conservation")),
        ("Other", _("Other")),
    )
    FORMER_LAND_COVER_CHOICES = (
        ("Cropland", _("Cropland")),
        ("Forest land", _("Forest land")),
        ("Pasture", _("Pasture")),
        ("Shrub land/Grassland", _("Shrub land/Grassland (Rangeland)")),
        ("Marginal land", _("Marginal land")),
        ("Wetland", _("Wetland")),
        ("Other land", _("Other land (e.g. developed land – specify in comment field)")),
    )

    form_title = _('Former use')

    tg_land_owner = TitleField(
        required=False, label="",
        initial=_("Former land owner (not by constitution)"))
    land_owner = forms.MultipleChoiceField(
        required=False, label=_("Former land owner"),
        choices=FORMER_LAND_OWNER_CHOICES, widget=forms.CheckboxSelectMultiple)
    tg_land_owner_comment = forms.CharField(
        required=False, label=_("Comment on former land owner"),
        widget=CommentInput)

    tg_land_use = TitleField(
        required=False, label="", initial=_("Former land use"))
    land_use = forms.MultipleChoiceField(
        required=False, label=_("Former land use"),
        choices=FORMER_LAND_USE_CHOICES, widget=forms.CheckboxSelectMultiple)
    tg_land_use_comment = forms.CharField(
        required=False, label=_("Comment on former land use"),
        widget=CommentInput)

    tg_land_cover = TitleField(
        required=False, label="", initial=_("Former land cover"))
    land_cover = forms.MultipleChoiceField(
        required=False, label=_("Former land cover"),
        choices=FORMER_LAND_COVER_CHOICES, widget=forms.CheckboxSelectMultiple)
    tg_land_cover_comment = forms.CharField(
        required=False, label=_("Comment on former land cover"),
        widget=CommentInput)

    class Meta:
        name = 'former_use'
