from django import forms
from django.utils.translation import ugettext_lazy as _

from registration.forms import RegistrationForm
from captcha.fields import ReCaptchaField
from .models.activity import Activity
from .models.region import Region


class CustomRegistrationForm(RegistrationForm):
    first_name = forms.CharField(label=_("First name"))
    last_name = forms.CharField(label=_("Last name"))
    phone = forms.CharField(label=_('Phone'), required=False)
    information = forms.CharField(label=_('User information'),
                                  help_text=_("Write something about yourself and your company. This won't be published."),
                                  widget=forms.Textarea)
    captcha = ReCaptchaField()

    #group, created = Group.objects.get_or_create(name='Reporters')
    #user.groups.add(group)
    #
    #UserRegionalInfo.objects.create(
    #    user=user,
    #    phone=form.cleaned_data['phone'],
    #    information=form.cleaned_data['information'],
    #)
    #
    #self.login(user)

    class Meta(RegistrationForm.Meta):
        fields = ('username', 'first_name', 'last_name', 'email', 'phone',
                  'information', 'password1', 'password2', 'captcha')


class ActivityFilterForm(forms.ModelForm):
    activity_identifier = forms.IntegerField(label=_("Deal ID"))
    target_region = forms.ModelChoiceField(label=_("Target region"), queryset=Region.objects.all())
    current_negotiation_status = forms.ChoiceField(label=_("Current negotiation status"),
                                                   choices=Activity.NEGOTIATION_STATUS_CHOICES)
    current_implementation_status = forms.ChoiceField(label=_("Current implementation status"),
                                                    choices=Activity.IMPLEMENTATION_STATUS_CHOICES)
    current_contract_size = forms.IntegerField(label=_("Current size under contract"))
    current_production_size = forms.IntegerField(label=_("Current size in operation (production)"))
    forest_concession = forms.BooleanField(label=_("Forest concession"))

    class Meta:
        model = Activity
        fields = ('activity_identifier', 'is_public', 'deal_scope', 'deal_size', 'init_date',
                  'fully_updated_date')
