from django.http import JsonResponse
from django.utils import timezone

from apps.message.models import Message


def messages_json(request):
    import ipdb; ipdb.set_trace()
    base_url = request.scheme + "://" + request.META['HTTP_HOST']
    is_internal_referer = 'HTTP_REFERER' in request.META and request.META[
        'HTTP_REFERER'].startswith(base_url)
    if is_internal_referer:
        msgs = []
    else:
        msgs = [
            msg.to_dict()
            for msg in Message.objects.filter(is_active=True).exclude(
                expires_at__lte=timezone.localdate()
            )
        ]
    return JsonResponse({"messages": msgs})
