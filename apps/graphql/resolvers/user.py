from typing import Type

from ariadne import ObjectType
from ariadne.graphql import GraphQLError

from django.contrib.auth import get_user_model

from apps.accounts.models import User

UserModel: Type[User] = get_user_model()


# noinspection PyShadowingBuiltins
def resolve_user(_obj, info, id=None):
    user = info.context["request"].user
    if not user.is_authenticated:
        return
    if user.is_staff and not info.field_name == "me":
        user = UserModel.objects.filter(is_staff=False).get(id=id)

    return user


def resolve_users(_obj, info, sort):
    user = info.context["request"].user
    if not (user.is_authenticated and user.role):
        raise GraphQLError("MISSING_AUTHORIZATION")

    users = UserModel.objects.filter(is_active=True).filter(role__gt=0)
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
