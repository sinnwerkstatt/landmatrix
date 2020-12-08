from django.http import JsonResponse
from django.utils import timezone

from apps.message.models import Message


def messages_json(request):
    msgs = [msg.to_dict() for msg in Message.objects.filter(is_active=True).exclude(
        expires_at__lte=timezone.localdate())]
    return JsonResponse({"messages": msgs})
