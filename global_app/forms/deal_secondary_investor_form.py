__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from .base_form import BaseForm
from global_app.widgets import CommentInput, TitleField, LivesearchSelect

from landmatrix.models.country import Country
from landmatrix.models.region import Region

from django import forms
from django.utils.translation import ugettext_lazy as _


class DealSecondaryInvestorForm(BaseForm):
    # Investor
    tg_investor = TitleField(required=False, label="", initial=_("Investor"))
    investor = forms.ChoiceField(required=False, label=_("Existing investor"), choices=(), widget=LivesearchSelect)
    investor_name = forms.CharField(required=False, label=_("Name"), max_length=255)
    country = forms.ChoiceField(required=False, label=_("Country"), choices=())
    region = forms.ModelChoiceField(required=False, label=_("Region"), widget=forms.HiddenInput, queryset=Region.objects.all().order_by('name'))
    classification = forms.ChoiceField(required=False, label=_("Classification"), choices=(
        (10, _("Private company")),
        (20, _("Stock-exchange listed company")),
        (30, _("Individual entrepreneur")),
        (40, _("Investment fund")),
        (50, _("Semi state-owned company")),
        (60, _("State-/government(-owned)")),
        (70, _("Other (please specify in comment field)")),
    ), widget=forms.RadioSelect)
    investment_ratio = forms.DecimalField(max_digits=19, decimal_places=2, required=False, label=_("Percentage of investment"), help_text=_("%"))
    tg_general_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)

    def __init__(self, *args, **kwargs):
        investor = kwargs.pop("investor", None)
        super(DealSecondaryInvestorForm, self).__init__(*args, **kwargs)
        self.fields["investor"].initial = investor
        # TODO: fix
        #self.investor_choices = Stakeholder.objects.raw_choices()
        self.investor_choices = []
        self.fields["investor"].choices = list(self.fields["investor"].choices)[:1]
        self.fields["investor"].choices.extend([(s.id, s) for s in self.investor_choices])
        self.fields["country"].choices = [
            ("", str(_("---------"))),
            (0, str(_("Multinational enterprise (MNE)")))
        ]
        self.fields["country"].choices.extend([(c.id, c.name) for c in Country.objects.all().order_by("name")])
        if self.DEBUG: print(self)

    def clean_investor(self):
        investor = int(self.cleaned_data["investor"] or 0)
        if investor and (investor not in [s.id for s in self.investor_choices]):
             raise forms.ValidationError("%s is no valid investor." % investor)
        return investor

    def clean(self):
        cleaned_data = super(DealSecondaryInvestorForm, self).clean()
        investor = cleaned_data.get("investor", None)
        investor_name = cleaned_data.get("investor_name", None)
        if not investor and not investor_name:
            raise forms.ValidationError("Please select an investor or investor name.")
        return cleaned_data

    def has_investor(self):
        if self.initial.get("investor"):
            return True
        elif self.is_valid() and self.cleaned_data.get("investor"):
            return True
        return False
