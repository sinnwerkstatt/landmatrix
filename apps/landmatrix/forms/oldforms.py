from captcha.fields import ReCaptchaField
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django_registration.forms import RegistrationForm

from apps.grid.fields import UserModelChoiceField
from apps.landmatrix.models import Country, HistoricalInvestor
from ..models import HistoricalActivity, Region


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


class ActivityFilterForm(forms.ModelForm):
    USER_QUERYSET = (
        get_user_model()
        .objects.filter(groups__name__in=("Editors", "Administrators"))
        .order_by("first_name", "last_name")
    )
    activity_identifier = forms.IntegerField(label=_("Deal ID"))
    is_public = forms.BooleanField(label=_("Is public"))
    deal_scope = forms.ChoiceField(
        label=_("Deal scope"), choices=HistoricalActivity.DEAL_SCOPE_CHOICES
    )
    deal_size = forms.IntegerField(label=_("Deal size"))
    init_date = forms.CharField(label=_("Initiation year or date"))
    target_region = forms.ModelChoiceField(
        label=_("Target region"), queryset=Region.objects.all()
    )
    current_negotiation_status = forms.ChoiceField(
        label=_("Current negotiation status"),
        choices=HistoricalActivity.NEGOTIATION_STATUS_CHOICES,
    )
    current_implementation_status = forms.ChoiceField(
        label=_("Current implementation status"),
        choices=HistoricalActivity.IMPLEMENTATION_STATUS_CHOICES,
    )
    current_contract_size = forms.IntegerField(label=_("Current size under contract"))
    current_production_size = forms.IntegerField(
        label=_("Current size in operation (production)")
    )
    forest_concession = forms.BooleanField(label=_("Forest concession"))
    updated_date = forms.DateField(label=("Last modification date"))
    updated_user = UserModelChoiceField(
        label=("Last modification by"), queryset=USER_QUERYSET
    )
    fully_updated_date = forms.DateField(label=("Fully updated date"))
    fully_updated_user = UserModelChoiceField(
        label=("Fully updated by"), queryset=USER_QUERYSET
    )
    top_investors = forms.CharField(label=_("Top investors"))

    class Meta:
        model = HistoricalActivity
        fields = (
            "activity_identifier",
            "is_public",
            "deal_scope",
            "deal_size",
            "init_date",
            "updated_date",
            "updated_user",
            "fully_updated_date",
            "fully_updated_user",
        )


class InvestorFilterForm(forms.ModelForm):
    investor_identifier = forms.IntegerField(label=_("Investor ID"))
    name = forms.CharField(label=_("Name"))
    fk_country = forms.ModelChoiceField(
        label=_("Country of registration/origin"), queryset=Country.objects.all()
    )
    classification = forms.ChoiceField(
        label=_("Classification"), choices=HistoricalInvestor.CLASSIFICATION_CHOICES
    )
    homepage = forms.URLField(label=_("Investor homepage"))
    opencorporates_link = forms.URLField(label=_("Opencorporates link"))
    comment = forms.CharField(label=_("Comment"), widget=forms.Textarea)
    top_investors = forms.CharField(label=_("Top investors"))
    deal_count = forms.IntegerField(label=_("Deals"))

    class Meta:
        model = HistoricalInvestor
        exclude = ("fk_status", "subinvestors")


class ExportActivityForm(forms.Form):
    activity_identifier = forms.IntegerField(label=_("Deal ID"))
    is_public = forms.BooleanField(label=_("Is public"))
    deal_scope = forms.CharField(label=_("Deal scope"))
    deal_size = forms.IntegerField(label=_("Deal size"))
    current_contract_size = forms.IntegerField(label=_("Current size under contract"))
    current_production_size = forms.IntegerField(
        label=_("Current size in operation (production)")
    )
    current_negotiation_status_display = forms.CharField(
        label=_("Current negotiation status")
    )
    current_implementation_status_display = forms.CharField(
        label=_("Current implementation status")
    )
    fully_updated_date = forms.DateField(label=_("Fully updated"))
    top_investors = forms.CharField(label=_("Top parent companies"))

    class Meta:
        model = HistoricalActivity
        exclude = ()
