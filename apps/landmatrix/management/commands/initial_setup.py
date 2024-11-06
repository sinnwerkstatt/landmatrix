import json
from typing import Type

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from wagtail.models import Page, Site

from apps.accounts.models import User
from apps.wagtailcms.models import (
    WagtailRootPage,
    AboutIndexPage,
    ObservatoryIndexPage,
)

UserModel: Type[User] = get_user_model()


def create_user(name, email, password, firstname, lastname, superuser=False):
    u_obj = UserModel.objects
    try:
        if superuser:
            user = u_obj.create_superuser(name, email, password)
        else:
            user = u_obj.create_user(name, email, password)
        user.first_name = firstname
        user.last_name = lastname
        user.save()
        return user
    except:
        pass


class Command(BaseCommand):
    @atomic
    def handle(self, *args, **options):
        print("  Creating Pages... ", end="", flush=True)
        # clear page tree
        root_page = Page.objects.first().get_root()
        root_page.title = "root"
        root_page.title_en = "root"
        root_page.save()
        root_page.get_children().delete()

        # reload root (as per https://github.com/wagtail/wagtail/issues/3402#issuecomment-297940917)
        root_page = Page.objects.first().get_root()

        wt_root = WagtailRootPage(
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
        root_page.add_child(instance=wt_root)
        wt_root.save()

        observatory_root = ObservatoryIndexPage(
            title="Global Observatory",
            slug="global",
        )
        wt_root.add_child(instance=observatory_root)
        observatory_root.save_revision().publish()

        about_root = AboutIndexPage(
            title="About",
            slug="about",
        )
        wt_root.add_child(instance=about_root)
        about_root.save_revision().publish()

        wt_root.save()

        # Reset site to localhost 900
        # TODO: This should only happen in in dev
        Site.objects.get_or_create(
            hostname="localhost",
            port=9000,
            root_page=wt_root,
            is_default_site=True,
        )
        print("\033[92m" + "OK" + "\033[0m")

        print("  Creating users... ", end="", flush=True)
        create_user(
            "landmatrixuser",
            "testuser@domain.tld",
            "landmatrix",
            "Land",
            "Matrix",
            superuser=True,
        )
        print("\033[92m" + "OK" + "\033[0m")
