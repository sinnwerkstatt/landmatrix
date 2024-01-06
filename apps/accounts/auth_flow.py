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

REGISTRATION_SALT = settings.SECRET_KEY

activation_email_body = """
Activate account at {{ site.name }}:

{{ scheme }}://{{ site.domain }}/account/activate/{{ activation_key }}/

Link is valid for {{ expiration_days }} days.
"""

activate_email_body_admin = """
A new user has registered and and waits for registration:

username: {{ user.username }}
email: {{ user.email }}
info: {{ user.information }}

{{ scheme }}://{{ site.domain }}/admin/accounts/user/{{ user.id }}/
"""


def _request_email_confirmation(user: User, request):
    """Ask for email confirmation from user."""
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


def _request_activation_from_user_admins(user: User, request):
    """Send mail to request account activation from user admins."""
    site = get_current_site(request)

    subject = f"A new user has registered on {site.name}"
    context = {
        "scheme": "https" if request.is_secure() else "http",
        "site": site,
        "user": user,
    }
    tmpl = Template(activate_email_body_admin)
    message = tmpl.render(Context(context))

    for user_admin in User.objects.filter(
        groups=Group.objects.get(name="User Management")
    ):
        user_admin.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)


def register(
    request,
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

    new_user = User.objects.create(
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

    _request_email_confirmation(new_user, request)
    return {"ok": True}


def register_confirm(request, activation_key):
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

    user = User.objects.get(username=username)
    if user.is_active:
        return {"ok": False, "code": "already_activated"}

    if not user.email_confirmed:
        user.email_confirmed = True
        user.save()

        _request_activation_from_user_admins(user, request)

    return {"ok": True}


def login(request, username, password) -> dict:
    if not User.objects.filter(username=username).exists():
        return {"ok": False, "error": _("Invalid username or password.")}
    if not User.objects.get(username=username).is_active:
        return {"ok": False, "error": _("Account not yet activated.")}

    user = auth.authenticate(request, username=username, password=password)
    if not user:
        return {"ok": False, "error": _("Invalid username or password.")}

    auth.login(request, user)
    return {"ok": True}


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return True
    return False


def password_reset(email, token) -> dict:
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
    # if len(list(form.get_users(email))) == 0:
    #     return {"ok": False, "code": "no_users_with_mail"}

    form.save()

    return {"ok": True}


def password_reset_confirm(uidb64, token, new_password1, new_password2) -> bool:
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (
        TypeError,
        ValueError,
        OverflowError,
        User.DoesNotExist,
        ValidationError,
    ) as e:
        print(e)
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
