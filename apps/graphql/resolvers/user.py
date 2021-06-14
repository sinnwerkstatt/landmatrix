from typing import Any

from ariadne import ObjectType
from ariadne.exceptions import HttpError
from django.contrib import auth
from graphql import GraphQLResolveInfo

from apps.graphql.resolvers.user_utils import get_user_role

User = auth.get_user_model()


def resolve_user(obj: Any, info: GraphQLResolveInfo, id=None):
    user = info.context["request"].user
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
    current_user = info.context["request"].user
    role = get_user_role(current_user)
    if role not in ["ADMINISTRATOR", "EDITOR"]:
        raise HttpError(message="Not allowed")

    users = User.objects.exclude(id=current_user.id)

    # this is implemented in Python, not in SQL, to support the "full_name"
    reverse = False
    if sort[0] == "-":
        reverse = True
        sort = sort[1:]
    return sorted(users, key=lambda u: u.__getattribute__(sort), reverse=reverse)


user_type = ObjectType("User")


@user_type.field("groups")
def get_user_groups(obj: User, info: GraphQLResolveInfo):
    return obj.groups.all()


@user_type.field("full_name")
def get_user_full_name(obj: User, info: GraphQLResolveInfo):
    full_name = (
        f"{obj.first_name} {obj.last_name}".strip()
        if (obj.first_name or obj.last_name)
        else obj.username
    )
    return full_name


user_regional_info_type = ObjectType("UserRegionalInfo")
user_regional_info_type.set_field("country", lambda obj, info: obj.country.all())
user_regional_info_type.set_field("region", lambda obj, info: obj.region.all())


def resolve_login(_, info, username, password) -> dict:
    request = info.context["request"]
    user = auth.authenticate(request, username=username, password=password)
    if user:
        auth.login(request, user)
        return {"status": True, "user": user}
    return {"status": False, "error": "Invalid username or password"}


def resolve_logout(_, info: GraphQLResolveInfo) -> bool:
    request = info.context["request"]
    if request.user.is_authenticated:
        auth.logout(request)
        return True
    return False
