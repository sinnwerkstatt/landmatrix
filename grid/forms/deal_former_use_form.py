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
            (_("State"), _("State")),
            (_("Private (smallholders)"), _("Private (smallholders)")),
            (_("Private (large-scale)"), _("Private (large-scale)")),
            (_("Community"), _("Community")),
            (_("Other"), _("Other")),
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
            (_("Commercial (large-scale) agriculture"), _("Commercial (large-scale) agriculture")),
            (_("Smallholder agriculture"), _("Smallholder agriculture")),
            (_("Shifting cultivation"), _("Shifting cultivation")),
            (_("Pastoralism"), _("Pastoralism")),
            (_("Hunting/Gathering"), _("Hunting/Gathering")),
            (_("Forestry"), _("Forestry")),
            (_("Conservation"), _("Conservation")),
            (_("Other"), _("Other")),
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
            (_("Cropland"), _("Cropland")),
            (_("Forest land"), _("Forest land")),
            (_("Pasture"), _("Pasture")),
            (_("Shrub land/Grassland (Rangeland)"), _("Shrub land/Grassland (Rangeland)")),
            (_("Marginal land"), _("Marginal land")),
            (_("Wetland"), _("Wetland")),
            (_("Other land[e.g. developed land – specify in comment field]"), _("Other land[e.g. developed land – specify in comment field]")),
        ), widget=forms.CheckboxSelectMultiple
    )
    tg_land_cover_comment = forms.CharField(
        required=False, label=_("Additional comments"), widget=CommentInput
    )

    class Meta:
        name = 'former_use'

