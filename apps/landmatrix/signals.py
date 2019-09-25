from django.contrib.auth.models import Group
from django_registration.signals import user_registered

from apps.editor.models import UserRegionalInfo


def create_userregionalinfo(sender, user, request, **kwargs):
    group, created = Group.objects.get_or_create(name="Reporters")
    user.groups.add(group)
    UserRegionalInfo.objects.create(
        user=user,
        phone=request.POST.get("phone", ""),
        information=request.POST.get("information", ""),
    )


user_registered.connect(create_userregionalinfo)
