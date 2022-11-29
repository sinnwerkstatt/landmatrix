from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from apps.accounts.models import UserRole

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(username="shakespeare").exists():
            will = User.objects.create_superuser(
                username="shakespeare",
                email="william@shakespeare.dev",
                password="hamlet4eva",
                first_name="William",
            )
            will.role = UserRole.ADMINISTRATOR
            cms_editors, _ = Group.objects.get_or_create(name="CMS Global (Editors)")
            will.groups.set([cms_editors])
            will.save()
            print("Created will")

        if not User.objects.filter(username="test_editor").exists():
            user = User.objects.create_user(
                username="test_editor",
                email="editor@test.dev",
                password="love2edit",
                first_name="Edith",
            )
            user.role = UserRole.EDITOR
            user.save()
            print("Created test editor")

        if not User.objects.filter(username="test_reporter").exists():
            user = User.objects.create_user(
                username="test_reporter",
                email="reporter@test.dev",
                password="love2report",
                first_name="Remi",
            )
            user.role = UserRole.REPORTER
            user.save()
            print("Created test reporter")
