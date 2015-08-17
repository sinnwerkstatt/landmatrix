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
    def get_data(cls, activity):
        #raise IOError, [{"investor": str(i.fk_stakeholder.id)} for i in activity.involvement_set.all()]
        data = []
        for i in activity.involvement_set.get_involvements_for_activity(activity):
            if not i.fk_stakeholder:
                continue
            comments = Comment.objects.filter(fk_sh_tag_group__fk_stakeholder=i.fk_stakeholder.id, fk_sh_tag_group__fk_sh_tag__fk_sh_value__value="General", fk_sh_tag_group__fk_sh_tag__fk_sh_key__key="name").order_by("-id")
            comment = ""
            if comments and len(comments) > 0:
                comment = comments[0].comment
            investor = {
                "investor": i.fk_stakeholder.id,
                "tg_general_comment": comment,
                "investment_ratio": i.investment_ratio,
            }
            data.append(investor)
        return data

