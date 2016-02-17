from global_app.forms.base_form import BaseForm
from global_app.forms.investor_form import InvestorField
from global_app.forms.operational_stakeholder_form import _investor_description

from landmatrix.models.investor import Investor

from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms.formsets import formset_factory

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class ParentStakeholderForm(BaseForm):

    stakeholder = InvestorField(required=False, label=_("Existing investor"), choices=())
    percentage = forms.DecimalField(
        max_digits=5, decimal_places=2, required=False, label=_("Percentage of investment"), help_text=_("%")
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        investor = kwargs.pop("stakeholder", None)
        self.fields["stakeholder"].initial = investor
        self._fill_investor_choices()

    def _fill_investor_choices(self):
        self.investor_choices = [
            (investor.id, _investor_description(investor))
            for investor in Investor.objects.filter(fk_status_id__in=(2, 3)).order_by('name')
        ]
        self.fields["stakeholder"].choices = list(self.fields["stakeholder"].choices)[:1]
        self.fields["stakeholder"].choices.extend(self.investor_choices)


class ParentStakeholderFormSet(formset_factory(ParentStakeholderForm, extra=1)):

    @classmethod
    def get_data(cls, investor):
        data = []
        return data

        involvements = deal.involvement_set().all() #get_involvements_for_activity(activity)
        for i, involvement in enumerate(involvements):
            if not involvement.fk_stakeholder:
                continue

            comments = Comment.objects.filter(
                fk_stakeholder_attribute_group__fk_stakeholder=involvement.fk_stakeholder,
                fk_stakeholder_attribute_group__attributes__contains={"name": "General" }
            ).order_by("-id")
            if comments:
                print('Whoa, look, comments:', comments)

            comment = comments[0].comment if comments and len(comments) > 0 else ''
            investor = {
                "investor": involvement.fk_stakeholder.id,
                "tg_general_comment": comment,
                "investment_ratio": involvement.investment_ratio,
            }
            data.append(investor)

        return data
