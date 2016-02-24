from landmatrix.models.investor import Investor

from .base_form import BaseForm
from grid.widgets import CommentInput, TitleField, LivesearchSelect

from landmatrix.models.country import Country
from landmatrix.models.region import Region

from django import forms
from django.utils.translation import ugettext_lazy as _

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class DealSecondaryInvestorForm(BaseForm):
    # Investor
    tg_investor = TitleField(required=False, label="", initial=_("Investor"))
    investor = forms.ChoiceField(required=False, label=_("Existing investor"), choices=())#, widget=LivesearchSelect)
    investor_name = forms.CharField(required=False, label=_("Name"), max_length=255)
    country = forms.ChoiceField(required=False, label=_("Country"), choices=())
    region = forms.ModelChoiceField(required=False, label=_("Region"), widget=forms.HiddenInput, queryset=Region.objects.all().order_by('name'))
    classification = forms.ChoiceField(
            required=False, label=_("Classification"), choices=Investor.classification_choices, widget=forms.RadioSelect
    )
    investment_ratio = forms.DecimalField(max_digits=19, decimal_places=2, required=False, label=_("Percentage of investment"), help_text=_("%"))
    tg_general_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)

    def __init__(self, *args, **kwargs):
        super(DealSecondaryInvestorForm, self).__init__(*args, **kwargs)
        investor = kwargs.pop("investor", None)
        self.fields["investor"].initial = investor
        self._fill_investor_choices()
        self._fill_country_choices()

    def clean_investor(self):
        investor = int(self.cleaned_data["investor"] or 0)
        if investor and (investor not in [s[0] for s in self.investor_choices]):
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

    def _fill_investor_choices(self):
        self.investor_choices = [
            (investor.id, self._investor_description(investor))
            for investor in Investor.objects.filter(fk_status_id__in=(2, 3)).order_by('name')
        ]
        self.fields["investor"].choices = list(self.fields["investor"].choices)[:1]
        self.fields["investor"].choices.extend(self.investor_choices)

    def _investor_description(self, investor):
        return investor.name + ' (' + self._investor_country_name(investor) + ')' + ' ' + self._investor_classification(investor)

    def _investor_country_name(self, investor):
        return Country.objects.get(pk=investor.fk_country_id).name if investor.fk_country_id else '-'

    def _investor_classification(self, investor):
        return investor.get_classification_display() if investor.classification else '-'

    def _fill_country_choices(self):
        self.fields["country"].choices = [
            ("", str(_("---------"))),
            (0, str(_("Multinational enterprise (MNE)")))
        ]
        self.fields["country"].choices.extend([(c.id, c.name) for c in Country.objects.all().order_by("name")])

