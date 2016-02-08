__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


from global_app.forms.base_form import BaseForm
from global_app.widgets import TitleField, CommentInput

from django import forms
from django.utils.translation import ugettext_lazy as _


class DealFormerUseForm(BaseForm):

    form_title = _('Former use')

    tg_land_owner = TitleField(required=False, label="", initial=_("Former land owner"))
    land_owner = forms.MultipleChoiceField(required=False, label=_("Former land owner"), choices=(
        (10, _("State")),
        (20, _("Private (smallholders)")),
        (30, _("Private (large-scale)")),
        (40, _("Community")),
        (50, _("Other")),
    ), widget=forms.CheckboxSelectMultiple)
    tg_land_owner_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)

    tg_land_use = TitleField(required=False, label="", initial=_("Former land use"))
    land_use = forms.MultipleChoiceField(required=False, label=_("Former land use"), choices=(
        (10, _("Commercial (large-scale) agriculture")),
        (20, _("Smallholder agriculture")),
        (30, _("Pastoralists")),
        (40, _("Forestry")),
        (50, _("Conservation")),
        (60, _("Other")),
    ), widget=forms.CheckboxSelectMultiple)
    tg_land_use_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)

    tg_land_cover = TitleField(required=False, label="", initial=_("Former land cover"))
    land_cover = forms.MultipleChoiceField(required=False, label=_("Former land cover"), choices=(
        (10, _("Cropland")),
        (20, _("Forest land")),
        (30, _("Shrub land/Grassland")),
        (40, _("Marginal land")),
        (50, _("Other land")),
    ), widget=forms.CheckboxSelectMultiple)
    tg_land_cover_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)

