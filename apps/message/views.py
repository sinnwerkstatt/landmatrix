from wagtailorderable.modeladmin.mixins import OrderableMixin

from django.utils import timezone
from rest_framework import serializers, viewsets
from wagtail.admin.viewsets.model import ModelViewSet
from wagtail.rich_text import expand_db_html

from apps.message.models import Message


class MessageAdminViewSet(OrderableMixin, ModelViewSet):
    model = Message
    menu_label = "Messages"
    icon = "pilcrow"
    # menu_order = 1000  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = True
    # form_fields = ["title", "text"]
    exclude_form_fields = []
    list_display = (
        "title",
        # "text",
        "level",
        "allow_users_to_hide",
        "logged_in_only",
        "is_active",
        "expires_at",
    )
    list_filter = ("level", "is_active")
    search_fields = ("title",)
    ordering = ["sort_order"]


message_viewset = MessageAdminViewSet("message")


class MessageSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()

    class Meta:
        model = Message
        exclude = ["sort_order", "expires_at"]
        read_only_fields = ["level", "logged_in_only", "allow_users_to_hide"]

    @staticmethod
    def get_text(obj) -> str:
        return expand_db_html(obj.text)


class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Message.objects.filter(is_active=True).exclude(
        expires_at__lte=timezone.localdate()
    )
    serializer_class = MessageSerializer
