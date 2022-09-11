from __future__ import annotations

from typing import Type

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from wagtail.core.models import Site

from apps.landmatrix.models.country import Country
from apps.landmatrix.models.deal import Deal
from apps.landmatrix.models.investor import Investor

User = get_user_model()


def get_user_role(user: User) -> str | None:
    roles = get_user_roles(user)
    return roles[0].upper() if roles else None


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


# TODO unused, but maybe helpful
def has_authorization_for_country(user: User, country: Country | int) -> bool:
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


def send_comment_to_user(
    obj: Deal | Investor,
    comment: str,
    from_user: User,
    to_user_id: int | Type[int],
    version_id: int = None,
) -> None:

    receiver = User.objects.get(id=to_user_id)
    subject = "[Landmatrix] " + _("New comment")
    full_name = from_user.get_full_name()

    obj_desc = (
        f"deal {obj.id}"
        if isinstance(obj, Deal)
        else f"investor {obj.name} (#{obj.id})"
    )

    if comment:
        message = _(f"{full_name} has addressed you in a comment on {obj_desc}:")
        message += "\n\n" + comment
    else:
        message = _(f"{full_name} has updated {obj_desc}:")

    site = Site.objects.get(is_default_site=True)

    port = f":{site.port}" if site.port not in [80, 443] else ""
    url = f"http{'s' if site.port == 443 else ''}://{site.hostname}{port}"

    is_deal = isinstance(obj, Deal)
    url += f"/deal/{obj.id}" if is_deal else f"/investor/{obj.id}"
    if version_id:
        url += f"/{version_id}"
    message += "\n\n" + _(f"Please review at {url}")

    receiver.email_user(subject, message, from_email=settings.DEFAULT_FROM_EMAIL)
