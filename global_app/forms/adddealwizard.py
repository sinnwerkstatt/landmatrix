
from global_app.widgets import *
from landmatrix.models import *

from .base_form import BaseForm

from django import forms
from django.utils.translation import ugettext_lazy as _

from django.utils.safestring import mark_safe
from django.utils.dateformat import DateFormat
from django.contrib.auth.models import User





class DealWaterForm(BaseForm):
    # Water extraction envisaged
    tg_water_extraction_envisaged = TitleField(required=False, label="", initial=_("Water extraction envisaged"))
    water_extraction_envisaged = forms.ChoiceField(required=False, label=_("Water extraction envisaged"), choices=(
        (10, _("Yes")),
        (20, _("No")),
    ), widget=forms.RadioSelect)
    tg_water_extraction_envisaged_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)
    # Source of water extraction
    tg_source_of_water_extraction = TitleField(required=False, label="", initial=_("Source of water extraction"))
    source_of_water_extraction = NestedMultipleChoiceField(required=False, label=_("Source of water extraction"), choices=(
        (10, _("Groundwater"), None),
        (20, _("Surface water"), (
           (21, _("River")),
           (22, _("Lake")),
        )),
    ))
    tg_source_of_water_extraction_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)
    # How much do investors pay for water and the use of water infrastructure?
    tg_how_much_do_investors_pay = TitleField(required=False, label="", initial=_("How much do investors pay for water and the use of water infrastructure?"))
    tg_how_much_do_investors_pay_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)
    # How much water is extracted?
    tg_water_extraction_amount = TitleField(required=False, label="", initial=_("How much water is extracted?"))
    water_extraction_amount = forms.IntegerField(required=False, label=_("Water extraction amount"), help_text=mark_safe(_("m&sup3;/year")), widget=NumberInput)
    tg_water_extraction_amount_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)

class DealGenderRelatedInfoForm(BaseForm):
    # Any gender-specific information about the investment and its impacts
    tg_gender_specific_info = TitleField(required=False, label="", initial=_("Any gender-specific information about the investment and its impacts"))
    tg_gender_specific_info_comment = forms.CharField(required=False, label="", widget=CommentInput)



class AddDealActionCommentForm(BaseForm):
    tg_action = TitleField(required=False, label="", initial=_("Action comment"))
    tg_action_comment = forms.CharField(required=False, label="", widget=CommentInput)
    fully_updated = forms.BooleanField(required=False, label=_("Fully updated"))
    fully_updated_history = forms.CharField(required=False, label=_("Fully updated history"), widget=forms.Textarea(attrs={"readonly":True, "cols": 80, "rows": 5}))


    tg_not_public = TitleField(required=False, label="", initial=_("Public deal"))
    not_public = forms.BooleanField(required=False, label=_("Not public"), help_text=_("Please specify in additional comment field"))
    not_public_reason = forms.ChoiceField(required=False, label=_("Reason"), choices=(
        (0, _("---------")),
        (10, _("Temporary removal from PI after criticism")),
        (20, _("Research in progress")),
    ))
    tg_not_public_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)

    tg_feedback = TitleField(required=False, label="", initial=_("Feedback"))
    assign_to_user = UserModelChoiceField(required=False, label=_("Assign to"), queryset=User.objects.filter(groups__name__in=("Research admins", "Research assistants")).order_by("username"), empty_label=_("Unassigned"))
    tg_feedback_comment = forms.CharField(required=False, label=_("Feedback comment"), widget=CommentInput)

    def get_action_comment(self):
        for j, taggroup in enumerate(super(AddDealActionCommentForm, self).get_taggroups()):
            if taggroup["main_tag"]["value"] == "action":
                return taggroup["comment"]
        return ""

    def get_feedback(self):
        for j, taggroup in enumerate(super(AddDealActionCommentForm, self).get_taggroups()):
            if taggroup["main_tag"]["value"] == "feedback":
                tags = taggroup.get("tags", [])
                if len(tags) > 0:
                    feedback = {
                        "assigned_to": tags[0].get("value"),
                        "comment": taggroup.get("comment")
                    }
                    return feedback
        return ""

    def get_fully_updated(self):
        for j, taggroup in enumerate(super(AddDealActionCommentForm, self).get_taggroups()):
            if taggroup["main_tag"]["value"] == "action":
                for tag in taggroup.get("tags", []):
                    if tag.get("key") == "fully_updated":
                        return tag.get("value")
        return False

    def get_taggroups(self, request=None):
        taggroups = []
        for tg in super(AddDealActionCommentForm, self).get_taggroups():
            if tg["main_tag"]["value"] in ("action", "feedback"):
                continue
            else:
                taggroups.append(tg)
        return taggroups

    @classmethod
    def get_data(cls, activity):
        data = super(AddDealActionCommentForm, cls).get_data(activity)
        a_feedback = A_Feedback.objects.filter(fk_activity=activity)
        if len(a_feedback) > 0:
            feedback = a_feedback[0]
            data.update({
                "assign_to_user": feedback.fk_user_assigned.id,
                "tg_feedback_comment": feedback.comment,
            })
        fully_updated_history = Activity.objects.get_fully_updated_history(activity.activity_identifier)
        fully_updated = []
        for h in fully_updated_history:
            fully_updated.append("%s - %s: %s" %(DateFormat(h.fully_updated).format("Y-m-d H:i:s"), h.username, h.comment))
        data.update({
            "fully_updated_history": "\n".join(fully_updated)
        })
        return data


class AddDealOverallCommentForm(BaseForm):
    # Coordinators and reviewers overall comments
    tg_overall = TitleField(required=False, label="", initial=_("Overall comment"))
    tg_overall_comment = forms.CharField(required=False, label="", widget=CommentInput)

class AddInvestorForm(BaseForm):
    tg_general = TitleField(required=False, label="", initial=_("General"))
    investor_name = forms.CharField(required=False, label=_("Name"), max_length=255)
    country = forms.ChoiceField(required=False, label=_("Country"), choices=())
    classification = forms.ChoiceField(required=False, label=_("Classification"), choices=(
        (10, _("Private company")),
        (20, _("Stock-exchange listed company")),
        (30, _("Individual entrepreneur")),
        (40, _("Investment fund")),
        (50, _("Semi state-owned company")),
        (60, _("State-/government(-owned)")),
        (70, _("Other (please specify in comment field)")),
    ), widget=forms.RadioSelect)
    tg_general_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)

    def __init__(self, *args, **kwargs):
        if kwargs.has_key("instance"):
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
        investor = long(self.cleaned_data["investor"] or 0)
        if investor and (investor not in [s.id for s in self.investor_choices]):
             raise forms.ValidationError("%s is no valid investor." % investor)
        return investor

    def get_taggroups(self, request=None):
        taggroups = super(AddInvestorForm, self).get_taggroups()
        return taggroups

class ManageDealForm(BaseForm):
    tg_action = TitleField(required=False, label="", initial=_("Action comment"))
    tg_action_comment = forms.CharField(required=False, label="", widget=CommentInput)

    def __init__(self, *args, **kwargs):
        if kwargs.has_key("instance"):
            kwargs.pop("instance")
        super(ManageDealForm, self).__init__(*args, **kwargs)

    def save(self):
        return self
