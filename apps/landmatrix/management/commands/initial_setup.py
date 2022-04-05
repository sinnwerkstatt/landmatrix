from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from wagtail.core.models import Page, Site

from apps.wagtailcms.models import WagtailPage, WagtailRootPage

User = get_user_model()


def create_user(name, email, password, firstname, lastname, superuser=False):
    u_obj = User.objects
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

        wt_root = WagtailRootPage(title="Land Matrix")
        root_page.add_child(instance=wt_root)
        wt_root.save()
        Site.objects.get_or_create(
            hostname="localhost", port=8000, root_page=wt_root, is_default_site=True
        )

        WagtailPage(title="Global Observatory", slug="global")

        # country_index = CountryIndex(title="Countries", slug="country")
        # wt_root.add_child(instance=country_index)
        # uganda = CountryPage(title="Uganda")
        # country_index.add_child(instance=uganda)
        #
        # region_index = RegionIndex(title="Regions", slug="region")
        # wt_root.add_child(instance=region_index)
        # asia = RegionPage(
        #     title="Asia", slug="asia", region=Region.objects.get(name="Asia")
        # )
        # region_index.add_child(instance=asia)

        print("\033[92m" + "OK" + "\033[0m")

        print("  Creating users... ", end="", flush=True)
        create_user(
            "landmatrixuser", "testuser@domain.tld", "landmatrix", "Land", "Matrix"
        )
        print("\033[92m" + "OK" + "\033[0m")
