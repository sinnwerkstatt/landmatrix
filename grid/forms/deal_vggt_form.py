__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from .base_form import BaseForm
from grid.widgets import CommentInput, TitleField, NestedMultipleChoiceField, NumberInput

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe


# Voluntary Guidelines on the Responsible Governance of Tenure
class DealVGGTForm(BaseForm):

    form_title = _(
        'Voluntary Guidelines on the Responsible Governance of Tenure (VGGT) / '
        'Principles for Responsible Agricultural Investments (PRAI)'
    )

    tg_vggt = TitleField(
        required=False, initial=_(
            "Voluntary Guidelines on the Responsible Governance of Tenure (VGGT) / "
            "Principles for Responsible Agricultural Investments (PRAI)"
        )
    )
    vggt_applied = forms.ChoiceField(
        required=False,
        label=_(
            "Application of Voluntary Guidelines on the Responsible Governance of Tenure (VGGT)"
        ),
        choices=(
            (_("Yes"), _("Yes")),
            (_("Partially"), _("Partially")),
            (_("No"), _("No")),
        ), widget=forms.RadioSelect
    )
    tg_vggt_applied_comment = forms.CharField(
        required=False, label=_("Additional comments"), widget=CommentInput
    )

    prai_applied = forms.ChoiceField(
        required=False,
        label=_("Application of Principles for Responsible Agricultural Investments (PRAI)"),
        choices=(
            (_("Yes"), _("Yes")),
            (_("Partially"), _("Partially")),
            (_("No"), _("No")),
        ), widget=forms.RadioSelect
    )
    tg_prai_applied_comment = forms.CharField(
        required=False, label=_("Additional comments"), widget=CommentInput
    )

    class Meta:
        name = 'vggt'
