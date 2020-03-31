from typing import Any

from django.contrib import auth
from graphql import GraphQLResolveInfo

User = auth.get_user_model()


def resolve_user(obj: Any, info: GraphQLResolveInfo, id=None):
    user = info.context.user
    if not user.is_authenticated:
        return
    if user.is_staff and not info.field_name == "me":
        user = User.objects.filter(is_staff=False).get(id=id)
    return user


def resolve_login(_, info, username, password):
    request = info.context
    user = auth.authenticate(request, username=username, password=password)
    if user:
        auth.login(request, user)
        return {"status": True, "user": user}
    return {"status": False, "error": "Invalid username or password"}


def resolve_logout(_, info: GraphQLResolveInfo):
    req = info.context
    if info.context.user.is_authenticated:
        auth.logout(req)
        return True
    return False
