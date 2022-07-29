import requests
from ariadne import ObjectType
from ariadne.exceptions import HttpError
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import AbstractUser
from django.contrib.sites.shortcuts import get_current_site
from django.core import signing
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode
from graphql import GraphQLError

from apps.editor.models import UserRegionalInfo
from apps.graphql.resolvers.user_utils import get_user_role

User: AbstractUser = auth.get_user_model()


# noinspection PyShadowingBuiltins
def resolve_user(_obj, info, id=None):
    user = info.context["request"].user
    if not user.is_authenticated:
        return
    if user.is_staff and not info.field_name == "me":
        user = User.objects.filter(is_staff=False).get(id=id)
    user.full_name = (
        f"{user.first_name} {user.last_name}".strip()
        if (user.first_name or user.last_name)
        else user.username
    )
    user.initials = (
        f"{user.first_name[0]}{user.last_name[0]}"
        if user.first_name and user.last_name
        else user.username[:2]
    )
    return user


def resolve_users(_obj, info, sort):
    current_user = info.context["request"].user
    role = get_user_role(current_user)
    if not role:
        raise GraphQLError(message="Not allowed")

    users = User.objects.filter(is_active=True).filter(
        groups__name__in=["Reporters", "Editors", "Administrators"]
    )
    # TODO - we could skip "reporters" here, and manually add the missing Reporter per deal in the frontend

    # this is implemented in Python, not in SQL, to support the "full_name"
    reverse = False
    if sort[0] == "-":
        reverse = True
        sort = sort[1:]
    return sorted(users, key=lambda u: u.__getattribute__(sort), reverse=reverse)


user_type = ObjectType("User")


@user_type.field("groups")
def get_user_groups(obj: User, _info):
    return obj.groups.all()


@user_type.field("role")
def get_user_r(obj: User, _info):
    return get_user_role(obj)


@user_type.field("full_name")
def get_user_full_name(obj: User, _info):
    full_name = (
        f"{obj.first_name} {obj.last_name}".strip()
        if (obj.first_name or obj.last_name)
        else obj.username
    )
    return full_name


user_regional_info_type = ObjectType("UserRegionalInfo")
user_regional_info_type.set_field("country", lambda obj, info: obj.country)
user_regional_info_type.set_field("region", lambda obj, info: obj.region)

REGISTRATION_SALT = getattr(settings, "REGISTRATION_SALT", "registration")


def send_activation_email(user, request):
    activation_key = signing.dumps(obj=user.get_username(), salt=REGISTRATION_SALT)
    context = {
        "scheme": "https" if request.is_secure() else "http",
        "activation_key": activation_key,
        "expiration_days": settings.ACCOUNT_ACTIVATION_DAYS,
        "site": get_current_site(request),
        "user": user,
    }
    subject = render_to_string(
        template_name="django_registration/activation_email_subject.txt",
        context=context,
        request=request,
    )
    # Force subject to a single line to avoid header-injection
    # issues.
    subject = "".join(subject.splitlines())
    message = render_to_string(
        template_name="django_registration/activation_email_body.txt",
        context=context,
        request=request,
    )
    user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)


def resolve_register(
    _obj,
    info,
    username,
    first_name,
    last_name,
    email,
    phone,
    information,
    password,
    token,
) -> dict:
    hcaptcha_verify = requests.post(
        "https://hcaptcha.com/siteverify",
        data={
            "response": token,
            "secret": settings.HCAPTCHA_SECRETKEY,
            "sitekey": settings.HCAPTCHA_SITEKEY,
        },
    ).json()
    if not hcaptcha_verify["success"]:
        return {"ok": False, "message": "captcha problems"}

    new_user = User.objects.create(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        is_active=False,
    )
    new_user.set_password(password)
    new_user.save()
    UserRegionalInfo.objects.create(user=new_user, phone=phone, information=information)

    send_activation_email(new_user, info.context["request"])
    return {"ok": True}
    # request = info.context["request"]
    # user = auth.authenticate(request, username=username, password=password)
    # if user:
    #     auth.login(request, user)
    #     return {"status": True, "user": user}
    # return {"status": False, "error": "Invalid username or password"}


def resolve_login(_obj, info, username, password) -> dict:
    request = info.context["request"]
    user = auth.authenticate(request, username=username, password=password)
    if user:
        auth.login(request, user)
        return {"status": True, "user": user}
    return {"status": False, "error": "Invalid username or password"}


def resolve_logout(_obj, info) -> bool:
    request = info.context["request"]
    if request.user.is_authenticated:
        auth.logout(request)
        return True
    return False


def resolve_password_reset(_obj, _info, email) -> bool:
    form = PasswordResetForm(data={"email": email})
    if form.is_valid():
        form.save()
        return True
    return False


def resolve_password_reset_confirm(
    _obj, _info, token, new_password1, new_password2
) -> bool:
    # This is currently not used. We should probably use a good lib here
    try:
        # urlsafe_base64_decode() decodes to bytestring
        uid = urlsafe_base64_decode(token).decode()
        user = User.objects.get(pk=uid)

    except User.DoesNotExist:
        return False
    form = SetPasswordForm(
        user=user,
        data={
            "new_password1": new_password1,
            "new_password2": new_password2,
        },
    )
    if form.is_valid():
        form.save()
        return True
    return False
