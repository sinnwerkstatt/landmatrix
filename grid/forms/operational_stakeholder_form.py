from django import forms
from django.forms.models import ModelChoiceField
from django.utils.translation import ugettext_lazy as _

from landmatrix.models.investor import Investor
from grid.forms.base_form import BaseForm
from grid.forms.choices import actor_choices
from grid.fields import TitleField, ActorsField
from grid.widgets import CommentInput, InvestorSelect


class OperationalStakeholderForm(BaseForm):
    exclude_in_export = ('operational_stakeholder',)

    form_title = _('Investor info')

    tg_operational_stakeholder = TitleField(
        required=False, label="", initial=_("Operating company"))
    operational_stakeholder = ModelChoiceField(
        required=False, label=_("Operating company"),
        queryset=Investor.objects.none(),
        widget=InvestorSelect(attrs={'class': 'form-control investorfield'}))
    actors = ActorsField(
        required=False,
        label=_("Actors involved in the negotiation / admission process"),
        choices=actor_choices)
    project_name = forms.CharField(
        required=False, label=_("Name of investment project"), max_length=255)
    tg_operational_stakeholder_comment = forms.CharField(
        required=False, label=_("Comment on Investment chain"),
        widget=CommentInput)

    @classmethod
    def get_data(cls, activity, group=None, prefix=""):
        data = super().get_data(activity, group, prefix)

        # Get operating company
        queryset = activity.involvements.order_by('-id')
        if queryset.count() > 0:
            data['operational_stakeholder'] = str(queryset[0].fk_investor.id)
        return data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Show given/current value only, rest happens via ajax
        valid_choice = self.data.get('operational_stakeholder',
                                     self.initial.get('operational_stakeholder', None))
        if valid_choice:
            field = self.fields['operational_stakeholder']
            field.queryset = Investor.objects.filter(pk=valid_choice)
            # Add investor identifier as data attribute
            if field.queryset.count() > 0:
                field.widget.data = {
                    str(valid_choice): {
                        'investor-identifier': field.queryset[0].investor_identifier
                    }
                }

    class Meta:
        name = 'investor_info'
