from django.contrib.auth.models import Group
from django.core.cache import cache
from django.db.models.signals import post_save
from django_registration.signals import user_registered

from apps.editor.models import UserRegionalInfo


# pylint: disable=unused-argument
def create_userregionalinfo(sender, user, request, **kwargs):
    group, created = Group.objects.get_or_create(name="Reporters")
    user.groups.add(group)
    UserRegionalInfo.objects.create(
        user=user,
        phone=request.POST.get("phone", ""),
        information=request.POST.get("information", ""),
    )


user_registered.connect(create_userregionalinfo)


def invalidate_cache(sender, instance, **kwargs):
    # FIXME it is quite brute force to just empty the whole cache. fixme "some day"™️
    cache.clear()


post_save.connect(invalidate_cache)
