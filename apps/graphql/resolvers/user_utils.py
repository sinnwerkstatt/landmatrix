from __future__ import annotations

from typing import Type

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from wagtail.core.models import Site

from apps.landmatrix.models.deal import Deal
from apps.landmatrix.models.investor import Investor

User = get_user_model()


# TODO unused, but maybe helpful
# def has_authorization_for_country(user: User, country: Country | int) -> bool:
#     if isinstance(country, int):
#         country = Country.objects.get(id=country)
#
#     if user.level == 3:
#         return True
#
#     if user.level >= 2:
#         if country == user.country:
#             return True
#         if user.region.country == country:
#             return True
#
#     return False


def send_comment_to_user(
    obj: Deal | Investor,
    comment: str,
    from_user: User,
    to_user_id: int | Type[int],
    version_id: int = None,
) -> None:

    receiver = User.objects.get(id=to_user_id)
    subject = "[Landmatrix] " + _("New comment")

    obj_desc = (
        f"deal {obj.id}"
        if isinstance(obj, Deal)
        else f"investor {obj.name} (#{obj.id})"
    )

    if comment:
        message = _(
            f"{from_user.full_name} has addressed you in a comment on {obj_desc}:"
        )
        message += "\n\n" + comment
    else:
        message = _(f"{from_user.full_name} has updated {obj_desc}:")

    site = Site.objects.get(is_default_site=True)

    port = f":{site.port}" if site.port not in [80, 443] else ""
    url = f"http{'s' if site.port == 443 else ''}://{site.hostname}{port}"

    is_deal = isinstance(obj, Deal)
    url += f"/deal/{obj.id}" if is_deal else f"/investor/{obj.id}"
    if version_id:
        url += f"/{version_id}"
    message += "\n\n" + _(f"Please review at {url}")

    receiver.email_user(subject, message, from_email=settings.DEFAULT_FROM_EMAIL)
