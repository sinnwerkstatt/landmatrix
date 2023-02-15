from django import forms
from django.utils.translation import gettext_lazy as _
from wagtail.users.forms import UserCreationForm, UserEditForm

from apps.landmatrix.models.country import Country, Region

from .models import User


class CustomUserEditForm(UserEditForm):
    role = forms.ChoiceField(required=False, label=_("Role"), choices=User.RoleChoices)
    country = forms.ModelChoiceField(required=False, queryset=Country.objects)
    region = forms.ModelChoiceField(required=False, queryset=Region.objects)


class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(required=False, label=_("Role"), choices=User.RoleChoices)
    country = forms.ModelChoiceField(required=False, queryset=Country.objects)
    region = forms.ModelChoiceField(required=False, queryset=Region.objects)
