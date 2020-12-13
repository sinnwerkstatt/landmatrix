from django import template
from django.utils import timezone

from apps.message.models import Message

register = template.Library()


@register.simple_tag(takes_context=True)
def custom_messages(context):
    request = context.request
    base_url = request.scheme + "://" + request.META['HTTP_HOST']
    is_internal_referer = 'HTTP_REFERER' in request.META and request.META[
        'HTTP_REFERER'].startswith(base_url)
    if is_internal_referer:
        return []
    else:
        return Message.objects.filter(is_active=True).exclude(
            expires_at__lte=timezone.localdate()
        )
