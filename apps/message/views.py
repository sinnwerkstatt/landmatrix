from wagtail.admin.viewsets.model import ModelViewSet
from wagtailorderable.modeladmin.mixins import OrderableMixin

from apps.message.models import Message


class MessageViewSet(OrderableMixin, ModelViewSet):
    model = Message
    menu_label = "Messages"
    icon = "pilcrow"
    # menu_order = 1000  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = True
    # form_fields = ["title", "text"]
    exclude_form_fields = []
    list_display = (
        "title",
        "text",
        "level",
        "allow_users_to_hide",
        "is_active",
        "expires_at",
    )
    list_filter = ("level", "is_active")
    search_fields = ("title",)
    ordering = ["sort_order"]


message_viewset = MessageViewSet("message")
