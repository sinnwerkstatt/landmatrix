import json

from django import template
from django.utils.html import escapejs

register = template.Library()


@register.simple_tag(takes_context=True)
def user_json(context):
    user = context["request"].user
    user_dict = {
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "full_name": f"{user.first_name} {user.last_name}".strip() or user.username,
        "is_authenticated": user.is_authenticated,
        "is_impersonate": user.is_impersonate,
    }
    return escapejs(json.dumps(user_dict))
