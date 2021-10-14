import requests
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from apps.graphql.resolvers.user_utils import get_user_role
from apps.public_comments.models import ThreadedComment


def resolve_add_public_comment(
    _, info, id, title, comment, token, name="", email=""
) -> bool:
    hcaptcha_verify = requests.post(
        "https://hcaptcha.com/siteverify",
        data={
            "response": token,
            "secret": settings.HCAPTCHA_SECRETKEY,
            "sitekey": settings.HCAPTCHA_SITEKEY,
        },
    ).json()
    if not hcaptcha_verify["success"]:
        return False

    tc = ThreadedComment(
        content_type=ContentType.objects.get(app_label="landmatrix", model="deal"),
        object_pk=id,
        title=title,
        comment=comment,
        site_id=settings.SITE_ID,
    )
    # TODO: Walrus this in python 3.8
    user = info.context["request"].user
    if user.is_authenticated:
        tc.user = user
    else:
        tc.user_name = name
        tc.user_email = email
    tc.save()
    return True


def resolve_remove_public_comment(_, info, id) -> bool:
    user = info.context["request"].user
    if get_user_role(user) == "ADMINISTRATOR":
        ThreadedComment.objects.filter(id=id).update(is_removed=True)
        return True
    return False
