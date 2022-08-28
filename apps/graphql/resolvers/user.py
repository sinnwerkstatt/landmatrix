from ariadne import ObjectType
from django.contrib import auth
from django.contrib.auth.models import AbstractUser
from ariadne.graphql import GraphQLError

from apps.graphql.resolvers.user_utils import get_user_role

User: AbstractUser = auth.get_user_model()


# noinspection PyShadowingBuiltins
def resolve_user(_obj, info, id=None):
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
    user.initials = (
        f"{user.first_name[0]}{user.last_name[0]}"
        if user.first_name and user.last_name
        else user.username[:2]
    )
    return user


def resolve_users(_obj, info, sort):
    current_user = info.context["request"].user
    role = get_user_role(current_user)
    if not role:
        raise GraphQLError(message="Not allowed")

    users = User.objects.filter(is_active=True).filter(
        groups__name__in=["Reporters", "Editors", "Administrators"]
    )
    # TODO - we could skip "reporters" here, and manually add the missing Reporter per deal in the frontend

    # this is implemented in Python, not in SQL, to support the "full_name"
    reverse = False
    if sort[0] == "-":
        reverse = True
        sort = sort[1:]
    return sorted(users, key=lambda u: u.__getattribute__(sort), reverse=reverse)


user_type = ObjectType("User")


@user_type.field("groups")
def get_user_groups(obj: User, _info):
    return obj.groups.all()


@user_type.field("role")
def get_user_r(obj: User, _info):
    return get_user_role(obj)


@user_type.field("full_name")
def get_user_full_name(obj: User, _info):
    full_name = (
        f"{obj.first_name} {obj.last_name}".strip()
        if (obj.first_name or obj.last_name)
        else obj.username
    )
    return full_name


user_regional_info_type = ObjectType("UserRegionalInfo")
user_regional_info_type.set_field("country", lambda obj, info: obj.country)
user_regional_info_type.set_field("region", lambda obj, info: obj.region)
