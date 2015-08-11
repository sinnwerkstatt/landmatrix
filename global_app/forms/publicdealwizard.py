
from django.utils.translation import ugettext_lazy as _
from django import forms

# TODO: fix
#from captcha.fields import ReCaptchaField

from global_app.forms.add_deal_employment_form import AddDealEmploymentForm
from global_app.forms.add_deal_general_form import AddDealGeneralForm
from global_app.forms.add_deal_overall_comment_form import AddDealOverallCommentForm
from global_app.widgets import TitleField, CommentInput


class AddDealGeneralPublicForm(AddDealGeneralForm):

    class Meta:

        fields = (
            "tg_land_area", "intended_size", "tg_land_area_comment",
            "tg_intention", "intention", "tg_intention_comment",
            "tg_implementation_status", "implementation_status", "tg_implementation_status_comment",
            "tg_negotiation_status", "negotiation_status", "tg_negotiation_status_comment",
            "tg_purchase_price", "purchase_price", "purchase_price_currency", "purchase_price_type", "purchase_price_area", "tg_purchase_price_comment",
            )

class DealEmploymentPublicForm(AddDealEmploymentForm):

    class Meta:

        fields = (
            "tg_foreign_jobs_created", "foreign_jobs_created", "foreign_jobs_planned", "tg_foreign_jobs_created_comment",
            "tg_domestic_jobs_created", "domestic_jobs_created", "domestic_jobs_planned", "tg_domestic_jobs_created_comment",
            )

class PublicUserInformationForm(AddDealOverallCommentForm):
    tg_public_user = TitleField(required=False, label="", initial=_("User information"))
    tg_public_user_comment = forms.CharField(
        required=True, label="", help_text=_("Write something about yourself and your company. This won't be published"), widget=CommentInput
    )
    public_user_name = forms.CharField(required=False, label=_("Name"))
    public_user_email = forms.EmailField(required=False, label=_("Email"))
    public_user_phone = forms.CharField(required=False, label=_("Phone"))
    # TODO: fix
#    captcha = ReCaptchaField()

    class Meta:
        exclude = ("tg_overall", "tg_overall_comment")

    def get_action_comment(self):
        action_comment = ""
        taggroups = super(PublicUserInformationForm, self).get_taggroups()
        if len(taggroups) > 0:
            taggroup = taggroups[0]
            action_comment += "comment: %s\n" % taggroup.get("comment", "-")
            for t in taggroup.get("tags", []):
                action_comment += "%s: %s\n" % (t.get("key").split("_")[-1], t.get("value"))
        return action_comment

    def get_taggroups(self, request=None):
            return []
