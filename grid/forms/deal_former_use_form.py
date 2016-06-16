from grid.forms.base_form import BaseForm
from grid.widgets import TitleField, CommentInput

from django import forms
from django.utils.translation import ugettext_lazy as _

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class DealFormerUseForm(BaseForm):

    form_title = _('Former use')

    tg_land_owner = TitleField(
        required=False, label="", initial=_("Former land owner (not by constitution)")
    )
    land_owner = forms.MultipleChoiceField(
        required=False, label=_("Former land owner"), choices=(
            ("State", _("State")),
            ("Private (smallholders)", _("Private (smallholders)")),
            ("Private (large-scale)", _("Private (large-scale farm)")),
            ("Community", _("Community")),
            ("Indigenous people", _("Indigenous people")),
            ("Other", _("Other")),
        ), widget=forms.CheckboxSelectMultiple
    )
    tg_land_owner_comment = forms.CharField(
        required=False, label=_("Additional comments"), widget=CommentInput
    )

    tg_land_use = TitleField(
        required=False, label="", initial=_("Former land use")
    )
    land_use = forms.MultipleChoiceField(
        required=False, label=_("Former land use"), choices=(
            ("Commercial (large-scale) agriculture", _("Commercial (large-scale) agriculture")),
            ("Smallholder agriculture", _("Smallholder agriculture")),
            ("Shifting cultivation", _("Shifting cultivation")),
            ("Pastoralism", _("Pastoralism")),
            ("Hunting/Gathering", _("Hunting/Gathering")),
            ("Forestry", _("Forestry")),
            ("Conservation", _("Conservation")),
            ("Other", _("Other")),
        ), widget=forms.CheckboxSelectMultiple
    )
    tg_land_use_comment = forms.CharField(
        required=False, label=_("Additional comments"), widget=CommentInput
    )

    tg_land_cover = TitleField(
        required=False, label="", initial=_("Former land cover")
    )
    land_cover = forms.MultipleChoiceField(
        required=False, label=_("Former land cover"), choices=(
            ("Cropland", _("Cropland")),
            ("Forest land", _("Forest land")),
            ("Pasture", _("Pasture")),
            ("Shrub land/Grassland (Rangeland)", _("Shrub land/Grassland (Rangeland)")),
            ("Marginal land", _("Marginal land")),
            ("Wetland", _("Wetland")),
            ("Other land[e.g. developed land – specify in comment field]", _("Other land[e.g. developed land – specify in comment field]")),
        ), widget=forms.CheckboxSelectMultiple
    )
    tg_land_cover_comment = forms.CharField(
        required=False, label=_("Additional comments"), widget=CommentInput
    )

    class Meta:
        name = 'former_use'

