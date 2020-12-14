from django import template
from django.utils import timezone

from apps.message.models import Message

register = template.Library()


@register.simple_tag(takes_context=True)
def custom_messages(context):
    request = context.request

    # only show warning messages when coming from internal referrer
    if "HTTP_HOST" in request.META:
        base_url = "https://" + request.META["HTTP_HOST"]
        if "HTTP_REFERER" in request.META:
            ref = request.META["HTTP_REFERER"]
            if ref.startswith("https://" + request.META["HTTP_HOST"]) or ref.startswith(
                "http://" + request.META["HTTP_HOST"]
            ):
                return Message.objects.filter(is_active=True).exclude(
                    expires_at__lte=timezone.localdate()
                ).filter(level=Message.LEVEL_WARNING)

    return Message.objects.filter(is_active=True).exclude(
        expires_at__lte=timezone.localdate()
    )
