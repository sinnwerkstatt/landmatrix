from django import forms
from django.utils.translation import ugettext_lazy as _

from registration.forms import RegistrationForm
from captcha.fields import ReCaptchaField


class CustomRegistrationForm(RegistrationForm):
    first_name = forms.CharField(label=_("First name"))
    last_name = forms.CharField(label=_("Last name"))
    phone = forms.CharField(label=_('Phone'), required=False)
    information = forms.CharField(label=_('User information'),
                                  help_text=_("Write something about yourself and your company. This won't be published."),
                                  widget=forms.Textarea)
    captcha = ReCaptchaField()

    class Meta(RegistrationForm.Meta):
        fields = ('first_name', 'last_name', 'email', 'phone', 'information', 'password1', 'password2', 'captcha')