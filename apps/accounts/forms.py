from django import forms
from django.utils.translation import gettext_lazy as _
from wagtail.users.forms import UserCreationForm, UserEditForm

from apps.landmatrix.models.country import Country, Region

from .models import UserRole


class CustomUserEditForm(UserEditForm):
    role = forms.ChoiceField(required=False, label=_("Role"), choices=UserRole.choices)
    country = forms.ModelChoiceField(required=False, queryset=Country.objects)
    region = forms.ModelChoiceField(required=False, queryset=Region.objects)

    class Meta(UserEditForm.Meta):
        fields = UserEditForm.Meta.fields | {"role", "country", "region"}


class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(required=False, label=_("Role"), choices=UserRole.choices)
    country = forms.ModelChoiceField(required=False, queryset=Country.objects)
    region = forms.ModelChoiceField(required=False, queryset=Region.objects)

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields | {"role", "country", "region"}
