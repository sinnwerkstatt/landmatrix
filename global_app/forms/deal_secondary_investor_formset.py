from pprint import pprint
from global_app.forms.base_form import BaseForm
from landmatrix.models.comment import Comment
from landmatrix.models.country import Country
from landmatrix.models.involvement import Involvement
from landmatrix.models.stakeholder_attribute_group import StakeholderAttributeGroup

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from global_app.forms.deal_secondary_investor_form import DealSecondaryInvestorForm

from django.forms.formsets import formset_factory

from copy import copy


BaseDealSecondaryInvestorFormSet = formset_factory(DealSecondaryInvestorForm, extra=0)


class DealSecondaryInvestorFormSet(BaseDealSecondaryInvestorFormSet):
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
        from inspect import currentframe, getframeinfo

        #raise IOError, [{"investor": str(i.fk_stakeholder.id)} for i in activity.involvement_set.all()]
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