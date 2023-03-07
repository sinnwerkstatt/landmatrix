from typing import Type

import requests

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core import signing
from django.core.exceptions import ValidationError
from django.template import Context, Template
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import User

UserModel: Type[User] = auth.get_user_model()

REGISTRATION_SALT = settings.SECRET_KEY

activation_email_body = """
Activate account at {{ site.name }}:

https://{{ site.domain }}/account/activate/{{ activation_key }}/

Link is valid for {{ expiration_days }} days.
"""


def _send_activation_email(user, request):
    activation_key = signing.dumps(obj=user.get_username(), salt=REGISTRATION_SALT)
    site = get_current_site(request)
    context = {
        "scheme": "https" if request.is_secure() else "http",
        "activation_key": activation_key,
        "expiration_days": settings.ACCOUNT_ACTIVATION_DAYS,
        "site": site,
        "user": user,
    }

    subject = _("Account activation on") + " " + site.name
    tmpl = Template(activation_email_body)
    message = tmpl.render(Context(context))
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
        return {"ok": False, "code": "captcha_problems"}

    new_user = UserModel.objects.create(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        information=information,
        is_active=False,
    )
    new_user.set_password(password)
    new_user.save()

    group, created = Group.objects.get_or_create(name="Reporters")
    new_user.groups.add(group)

    _send_activation_email(new_user, info.context["request"])
    return {"ok": True}


def resolve_register_confirm(_obj, _info, activation_key):
    try:
        username = signing.loads(
            activation_key,
            salt=REGISTRATION_SALT,
            max_age=settings.ACCOUNT_ACTIVATION_DAYS * 86400,
        )
    except signing.SignatureExpired:
        return {"ok": False, "code": "expired"}
    except signing.BadSignature:
        return {"ok": False, "code": "invalid_key"}
    user = UserModel.objects.get(username=username)
    if user.email_confirmed or user.is_active:
        return {"ok": False, "code": "already_activated"}
    user.email_confirmed = True
    user.save()
    return {"ok": True, "user": user}


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


def resolve_password_reset(_obj, _info, email, token) -> dict:
    hcaptcha_verify = requests.post(
        "https://hcaptcha.com/siteverify",
        data={
            "response": token,
            "secret": settings.HCAPTCHA_SECRETKEY,
            "sitekey": settings.HCAPTCHA_SITEKEY,
        },
    ).json()

    if not hcaptcha_verify["success"]:
        return {"ok": False, "code": "captcha_problems"}

    form = PasswordResetForm(data={"email": email})
    if not form.is_valid():
        return {"ok": False, "code": f"form_validation_error: {form.errors}"}
    if len(list(form.get_users(email))) == 0:
        return {"ok": False, "code": "no_users_with_mail"}

    try:
        form.save()
    except:
        return {"ok": False, "code": "form_save_error"}
    return {"ok": True}


def resolve_password_reset_confirm(
    _obj, _info, uidb64, token, new_password1, new_password2
) -> bool:
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel.objects.get(pk=uid)
    except (
        TypeError,
        ValueError,
        OverflowError,
        UserModel.DoesNotExist,
        ValidationError,
    ):
        return False

    if user and default_token_generator.check_token(user, token):
        form = SetPasswordForm(
            user=user,
            data={"new_password1": new_password1, "new_password2": new_password2},
        )
        if form.is_valid():
            form.save()
            return True
    return False
