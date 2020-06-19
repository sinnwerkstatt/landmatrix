from typing import Any

from ariadne import ObjectType
from ariadne.exceptions import HttpError
from django.contrib import auth
from graphql import GraphQLResolveInfo

User = auth.get_user_model()


def resolve_user(obj: Any, info: GraphQLResolveInfo, id=None):
    user = info.context.user
    if not user.is_authenticated:
        return
    if user.is_staff and not info.field_name == "me":
        user = User.objects.filter(is_staff=False).get(id=id)
    user.full_name = (
        f"{user.first_name} {user.last_name}".strip()
        if (user.first_name or user.last_name)
        else user.username
    )
    return user


def resolve_users(obj: Any, info: GraphQLResolveInfo, sort):
    current_user = info.context.user
    if not current_user.is_staff:
        raise HttpError(message="Not allowed")

    users = User.objects.exclude(id=current_user.id)
    for user in users:
        user.full_name = (
            f"{user.first_name} {user.last_name}".strip()
            if (user.first_name or user.last_name)
            else user.username
        )

    # this is implemented in Python, not in SQL, to support the "full_name"
    reverse = False
    if sort[0] == "-":
        reverse = True
        sort = sort[1:]
    return sorted(users, key=lambda u: u.__getattribute__(sort), reverse=reverse)


user_regional_info_type = ObjectType("UserRegionalInfo")
user_regional_info_type.set_field("country", lambda obj, info: obj.country.all())
user_regional_info_type.set_field("region", lambda obj, info: obj.region.all())


def resolve_login(_, info, username, password):
    request = info.context
    user = auth.authenticate(request, username=username, password=password)
    if user:
        auth.login(request, user)
        user.full_name = (
            f"{user.first_name} {user.last_name}".strip()
            if (user.first_name or user.last_name)
            else user.username
        )
        return {"status": True, "user": user}
    return {"status": False, "error": "Invalid username or password"}


def resolve_logout(_, info: GraphQLResolveInfo):
    req = info.context
    if info.context.user.is_authenticated:
        auth.logout(req)
        return True
    return False
