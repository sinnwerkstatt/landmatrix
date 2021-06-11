from typing import Union

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
from wagtail.core.models import Site

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


def send_comment_to_user(deal, comment, from_user, to_user_id, version_id=None):
    receiver = User.objects.get(id=to_user_id)
    subject = "[Landmatrix] " + _("New comment")
    if comment:
        message = _(
            f"{from_user.get_full_name()} has addressed you in a comment on deal {deal.id}:"
        )
        message += "\n\n" + comment
    else:
        message = _(f"{from_user.get_full_name()} has updated deal {deal.id}:")

    site = Site.objects.get(is_default_site=True)
    url = f"http{'s' if site.port == 444 else ''}://{site.hostname}"
    if site.port not in [80, 443]:
        url += f":{site.port}"
    url += f"/deal/{deal.id}"
    if version_id:
        url += f"/{version_id}"
    message += "\n\n" + _(f"Please review at {url}")

    receiver.email_user(subject, message, from_email=settings.DEFAULT_FROM_EMAIL)
