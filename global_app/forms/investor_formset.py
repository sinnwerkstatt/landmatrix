from pprint import pprint

from django.core.exceptions import ValidationError

from global_app.forms.base_form import BaseForm
from global_app.forms.operational_stakeholder_form import _investor_description
from landmatrix.models.comment import Comment

from landmatrix.models.investor import Investor, InvestorActivityInvolvement

from global_app.widgets import CommentInput, TitleField, LivesearchSelect

from landmatrix.models.country import Country
from landmatrix.models.region import Region

from django import forms
from django.utils.translation import ugettext_lazy as _

from django.forms.formsets import formset_factory

from copy import copy

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class InvestorChoicesMixin:

    def __init__(self, *args, **kwargs):
        investor = kwargs.pop("investor", None)
        self.fields["investor"].initial = investor
        self._fill_investor_choices()

    def _fill_investor_choices(self):
        self.investor_choices = [
            (investor.id, _investor_description(investor))
            for investor in Investor.objects.filter(fk_status_id__in=(2, 3)).order_by('name')
        ]
        self.fields["investor"].choices = list(self.fields["investor"].choices)[:1]
        self.fields["investor"].choices.extend(self.investor_choices)


# Change this to a livesearch widget once you got a working one
InvestorField = forms.ChoiceField


class InvestorForm(BaseForm, InvestorChoicesMixin):

    # Investor
    tg_investor = TitleField(required=False, label="", initial=_("Investor"))
    investor = InvestorField(required=False, label=_("Existing investor"), choices=())#, widget=LivesearchSelect)
    investor_name = forms.CharField(required=False, label=_("Name"), max_length=255)
    country = forms.ChoiceField(required=False, label=_("Country"), choices=())
    region = forms.ModelChoiceField(required=False, label=_("Region"), widget=forms.HiddenInput, queryset=Region.objects.all().order_by('name'))
    classification = forms.ChoiceField(
            required=False, label=_("Classification"), choices=Investor.classification_choices, widget=forms.RadioSelect
    )
    investment_ratio = forms.DecimalField(max_digits=19, decimal_places=2, required=False, label=_("Percentage of investment"), help_text=_("%"))
    tg_general_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        cleaned_data = super().clean()
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

    def _fill_country_choices(self):
        self.fields["country"].choices = [
            ("", str(_("---------"))),
            (0, str(_("Multinational enterprise (MNE)")))
        ]
        self.fields["country"].choices.extend([(c.id, c.name) for c in Country.objects.all().order_by("name")])


class ParentStakeholderForm(BaseForm, InvestorChoicesMixin):

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

ParentStakeholderFormSet = formset_factory(ParentStakeholderForm, extra=1)

BaseInvestorFormSet = formset_factory(InvestorForm, extra=1)


class InvestorFormSet(BaseInvestorFormSet):

    def get_taggroups(self, request=None):
        return []

    def get_stakeholders(self):
        stakeholders = []
        for i, form in enumerate(self.forms):
            stakeholder = {}
            for j, taggroup in enumerate(form.get_taggroups()):
                comment = taggroup.get("comment", "")
                for i, t in reversed(list(enumerate(taggroup["tags"]))):
                    if t["key"] == "investor":
                        # Existing investor
                        stakeholder["investment_ratio"] = str(taggroup["investment_ratio"])
                        stakeholder["id"] = t["value"]
                        stakeholder["taggroups"] = [{
                            "main_tag": {"key": "name", "value": "General"},
                            "comment": comment,
                        }]
                if not stakeholder:
                    stakeholder["investment_ratio"] = taggroup["investment_ratio"]
                    stakeholder["taggroups"] = [{
                        "main_tag": {"key": "name", "value": "General"},
                        "tags": taggroup["tags"],
                        "comment": comment,
                    }]
            if stakeholder:
                stakeholders.append(copy(stakeholder))
        return stakeholders


    @classmethod
    def get_data(cls, deal):
        data = []
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


def get_investors(deal):
    return {
        'primary_investor': get_primary_investor(deal),
        'secondary_investors': get_secondary_investors(deal)
    }


def get_primary_investor(deal):
    return deal.primary_investor


def get_secondary_investors(deal):
    return [
        {
            'investment_ratio': Involvement.objects.filter(fk_stakeholder=sh).first().investment_ratio,
            'tags': get_tags(sh),
            'comment': get_stakeholder_comments(sh)
        } for sh in deal.stakeholders
        ]


def get_tags(sh):
    return {
        key: resolve_country(key, value)
        for key, value in StakeholderAttributeGroup.objects.filter(fk_stakeholder=sh).first().attributes.items()
    }


def get_stakeholder_comments(stakeholder):
    attribute_group = StakeholderAttributeGroup.objects.filter(fk_stakeholder=stakeholder).order_by('id').last()
    return Comment.objects.filter(
            fk_stakeholder_attribute_group=attribute_group
        ).exclude(
            comment=''
        ).order_by('-timestamp').values_list('comment', flat=True).first()


def resolve_country(key, value):
    if key != 'country': return value
    if not value.isdigit(): return value
    return Country.objects.get(id=value).name