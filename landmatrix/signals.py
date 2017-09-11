from django.contrib.auth.models import User, Group

from registration.signals import user_registered

from editor.models import UserRegionalInfo

def create_userregionalinfo(sender, user, request, **kwarg):
    group, created = Group.objects.get_or_create(name='Reporters')
    user.groups.add(group)
    UserRegionalInfo.objects.create(
        user=user,
        phone=request.POST.get('phone', ''),
        information=request.POST.get('information', ''),
    )
user_registered.connect(create_userregionalinfo)