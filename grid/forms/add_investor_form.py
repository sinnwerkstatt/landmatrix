from landmatrix.models.investor import Investor

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from grid.forms.base_form import BaseForm
from grid.widgets import TitleField, CommentInput
from landmatrix.models.country import Country

from django import forms
from django.utils.translation import ugettext_lazy as _


class AddInvestorForm(BaseForm):
    tg_general = TitleField(required=False, label="", initial=_("General"))
    investor_name = forms.CharField(required=False, label=_("Name"), max_length=255)
    country = forms.ChoiceField(required=False, label=_("Country"), choices=())
    classification = forms.ChoiceField(
            required=False, label=_("Classification"), choices=Investor.classification_choices, widget=forms.RadioSelect
    )
    tg_general_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)

    def __init__(self, *args, **kwargs):
        if "instance" in kwargs:
            kwargs["initial"] = self.get_data(kwargs.pop("instance"))
        super(AddInvestorForm, self).__init__(*args, **kwargs)
        self.fields["country"].choices = [
            ("", str(_("---------"))),
            (0, str(_("Multinational enterprise (MNE)")))
        ]
        self.fields["country"].choices.extend([(c.id, c.name) for c in Country.objects.all().order_by("name")])

    def save(self):
        return self

    def clean_investor(self):
        investor = int(self.cleaned_data["investor"] or 0)
        if investor and (investor not in [s.id for s in self.investor_choices]):
             raise forms.ValidationError("%s is no valid investor." % investor)
        return investor

    def get_attributes(self, request=None):
        taggroups = super(AddInvestorForm, self).get_attributes()
        return taggroups
