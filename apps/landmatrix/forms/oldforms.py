from captcha.fields import ReCaptchaField
from django import forms
from django.utils.translation import gettext_lazy as _
from django_registration.forms import RegistrationForm


class CustomRegistrationForm(RegistrationForm):
    first_name = forms.CharField(label=_("First name"))
    last_name = forms.CharField(label=_("Last name"))
    phone = forms.CharField(label=_("Phone"), required=False)
    information = forms.CharField(
        label=_("User information"),
        help_text=_(
            "Write something about yourself and your company. This won't be published."
        ),
        widget=forms.Textarea,
    )
    captcha = ReCaptchaField()

    # group, created = Group.objects.get_or_create(name='Reporters')
    # user.groups.add(group)
    #
    # UserRegionalInfo.objects.create(
    #    user=user,
    #    phone=form.cleaned_data['phone'],
    #    information=form.cleaned_data['information'],
    # )
    #
    # self.login(user)

    class Meta(RegistrationForm.Meta):
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "information",
            "password1",
            "password2",
            "captcha",
        )
