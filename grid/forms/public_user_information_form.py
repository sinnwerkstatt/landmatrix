from django import forms
from django.utils.translation import ugettext_lazy as _
from captcha.fields import ReCaptchaField

from grid.forms.base_form import BaseForm
from grid.fields import TitleField
from grid.widgets import CommentInput


class PublicUserInformationForm(BaseForm):
    form_title = _('User information')
    form_description = _('Your contact information will help our researchers get in touch with you for additional information. We respect and protect your privacy and anonymity, and will never share or publish your personal information. You can also write us directly at data@landmatrix.org.')

    tg_public_user = TitleField(
        required=False, label="", initial=_("User information"))
    tg_action_comment = forms.CharField(
        required=True, label="",
        help_text=_("Write something about yourself and your company. This won't be published."),
        widget=CommentInput)
    public_user_name = forms.CharField(required=False, label=_("Name"))
    public_user_email = forms.EmailField(required=True, label=_("Email"))
    public_user_phone = forms.CharField(required=False, label=_("Phone"))
    captcha = ReCaptchaField()

    #def get_action_comment(self):
    #    action_comment = ""
    #    groups = super(PublicUserInformationForm, self).get_attributes()
    #    if len(groups) > 0:
    #        group = groups[0]
    #        action_comment += "comment: %s\n" % group.get("tg_public_user_comment", "-")
    #        for t in group.get("tags", []):
    #            action_comment += "%s: %s\n" % (
    #                t.get("key").split("_")[-1], t.get("value")
    #            )
    #    return action_comment

    def get_attributes(self, request=None):
        return {}

    class Meta:
        name = 'user_information'
