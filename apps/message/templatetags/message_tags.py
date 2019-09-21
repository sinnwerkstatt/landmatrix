from django import template

from apps.message.models import Message

register = template.Library()


@register.simple_tag
def custom_messages():
    return Message.objects.filter(is_active=True)
