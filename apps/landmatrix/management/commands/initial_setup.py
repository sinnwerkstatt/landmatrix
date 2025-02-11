import json
import os.path
import secrets
import string
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db.transaction import atomic
from wagtail.models import Page, Site

from apps.wagtailcms.models import AboutIndexPage, ObservatoryIndexPage, WagtailRootPage

User = get_user_model()


class Command(BaseCommand):
    @atomic
    def handle(self, *args, **options):
        if User.objects.all().count() > 0:
            print(
                "The database already has content. If you would like to reset it, run:"
            )
            print("doit -n1 reset_db migrate")
            raise CommandError("database dirty")

        create_pages()
        create_user()


def create_pages(port=9000):
    print("  Creating Pages... ", flush=True)

    # clear page tree
    root_page = Page.objects.first().get_root()
    root_page.title = "root"
    root_page.title_en = "root"
    root_page.save()
    root_page.get_children().delete()

    # reload root
    root_page = Page.objects.get(path="0001")
    home_page = WagtailRootPage(
        title="Land Matrix",
        body=json.dumps(
            [
                {
                    "type": "section_divider",
                    "value": {},
                    "id": "6761c639-41b0-4b11-a0c0-31a730d45e71",
                }
            ]
        ),
    )

    root_page.add_child(instance=home_page)
    home_page.save()

    observatory_root = ObservatoryIndexPage(
        title="Global Observatory",
        slug="global",
    )
    home_page.add_child(instance=observatory_root)
    observatory_root.save_revision().publish()

    about_root = AboutIndexPage(
        title="About",
        slug="about",
    )
    home_page.add_child(instance=about_root)
    about_root.save_revision().publish()

    home_page.save()

    site, _ = Site.objects.get_or_create(
        hostname="localhost",
        port=port,
        root_page=home_page,
        is_default_site=True,
    )

    print("  Creating Pages... \033[92m" + "OK" + "\033[0m\n", flush=True)


def create_user():
    print("  Creating User... ", flush=True)

    my_django_superuser_file = Path.home() / ".my-django-superuser"

    user = {
        "username": "support@sinnwerkstatt.com",
        "email": "support@sinnwerkstatt.com",
        "first_name": "Support",
        "last_name": "Sinnwerkstatt",
    }

    if os.path.exists(my_django_superuser_file):
        with open(my_django_superuser_file) as f:
            user = json.load(f)
        print(
            f"  Found ~/.my-django-superuser. username: {user['username']}, email: {user['email']}"
        )
    else:
        print(
            f"  No ~/.my-django-superuser file. username: {user['username']}, email: {user['email']}"
        )

    if not user.get("password"):
        user["password"] = _generate_password()
        print(
            f"  No password specified, using random password: \033[1;33m{user['password']}\033[0m"
        )

    User.objects.create_superuser(
        user["username"],
        user["email"],
        user["password"],
        first_name=user["first_name"],
        last_name=user["last_name"],
    )

    print("  Creating User... \033[92m" + "OK" + "\033[0m\n", flush=True)


def _generate_password():
    n_digits = 20
    alphabet = string.ascii_letters + string.digits + ".,_-=+;:"
    return "".join(secrets.choice(alphabet) for _ in range(n_digits))
