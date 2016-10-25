from django import forms
from django.utils.translation import ugettext_lazy as _

from grid.fields import TitleField
from grid.widgets import CommentInput
from .base_form import BaseForm


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class DealVGGTForm(BaseForm):
    '''
    Voluntary Guidelines on the Responsible Governance of Tenure Form.
    '''
    form_title = _('Guidelines & Principles')
    APPLIED_CHOICES = (
        ("Yes", _("Yes")),
        ("Partially", _("Partially")),
        ("No", _("No")),
    )

    tg_vggt = TitleField(
        required=False,
        initial=_("Voluntary Guidelines on the Responsible Governance of Tenure (VGGT)"))
    vggt_applied = forms.ChoiceField(
        required=False,
        label=_("Application of Voluntary Guidelines on the Responsible Governance of Tenure (VGGT)"),
        choices=APPLIED_CHOICES, widget=forms.RadioSelect)
    tg_vggt_applied_comment = forms.CharField(
        required=False, label=_("Comment on VGGT"), widget=CommentInput)

    tg_prai = TitleField(
        required=False,
        initial=_("Principles for Responsible Agricultural Investments (PRAI)"))
    prai_applied = forms.ChoiceField(
        required=False,
        label=_("Application of Principles for Responsible Agricultural Investments (PRAI)"),
        choices=APPLIED_CHOICES, widget=forms.RadioSelect)
    tg_prai_applied_comment = forms.CharField(
        required=False, label=_("Comment on PRAI"), widget=CommentInput)

    class Meta:
        name = 'vggt'
