from .models import Message


def add_custom_messages(request):
    context = dict()
    context['custom_messages'] = Message.objects.active()
    return context
