from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(username='shakespeare').exists():
            will = User.objects.create_superuser('shakespeare', 'william@shakespeare.dev', 'hamlet4eva')
            will.level = 3
            cms_editors, _ = Group.objects.get_or_create(name="CMS Global (Editors)")
            will.groups.set([cms_editors])
            will.save()
            print('Created will')

        if not User.objects.filter(username='test_editor').exists():
            user = User.objects.create_user('test_editor', 'editor@test.dev', 'love2edit')
            user.level = 2
            user.save()
            print('Created test editor')

        if not User.objects.filter(username='test_reporter').exists():
            user = User.objects.create_user('test_reporter', 'reporter@test.dev', 'love2report')
            user.level = 1
            user.save()
            print('Created test reporter')
