from django.http import JsonResponse

from apps.message.models import Message


def messages_json(request):
    msgs = [msg.to_dict() for msg in Message.objects.filter(is_active=True)]
    return JsonResponse({"messages": msgs})
