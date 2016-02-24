__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from grid.forms.add_deal_overall_comment_form import AddDealOverallCommentForm
from grid.widgets import TitleField, CommentInput

from django import forms
from django.utils.translation import ugettext_lazy as _

# TODO: fix
#from captcha.fields import ReCaptchaField


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
