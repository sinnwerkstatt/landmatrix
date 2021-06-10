from typing import Union

from django.contrib.auth import get_user_model

from apps.landmatrix.models import Country

User = get_user_model()


def get_user_roles(user: User) -> list:
    return [
        x[:-1]
        for x in user.groups.filter(name__in=["Administrators", "Editors", "Reporters"])
        .values_list("name", flat=True)
        .order_by("name")  # so that the highest rank comes first
    ]


def get_user_roc_and_role(user: User) -> dict:
    output = {"roles": get_user_roles(user)}

    if hasattr(user, "userregionalinfo"):
        output["roc"] = list(
            user.userregionalinfo.country.values_list("name", flat=True)
        ) + list(user.userregionalinfo.region.values_list("name", flat=True))
    else:
        output["roc"] = []
    return output


def has_authorization_for_country(user: User, country: Union[Country, int]) -> bool:
    if isinstance(country, int):
        country = Country.objects.get(id=country)

    roles = get_user_roles(user)
    if "Administrator" in roles:
        return True

    if not hasattr(user, "userregionalinfo"):
        return False

    if "Editor" in roles:
        if country in user.userregionalinfo.country.all():
            return True
        if user.userregionalinfo.region.filter(country=country).exists():
            return True

    return False
