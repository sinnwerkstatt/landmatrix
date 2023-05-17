from wagtailorderable.modeladmin.mixins import OrderableMixin

from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail import hooks
from wagtail.whitelist import attribute_rule

from apps.message.models import Message


@hooks.register("register_icons")
def register_icons(icons):
    return icons + [
        "wagtailfontawesomesvg/brands/twitter.svg",
        "wagtailfontawesomesvg/solid/arrows-alt-h.svg",
        "wagtailfontawesomesvg/solid/columns.svg",
        "wagtailfontawesomesvg/solid/flag.svg",
        "wagtailfontawesomesvg/solid/folder.svg",
        "wagtailfontawesomesvg/solid/image.svg",
        "wagtailfontawesomesvg/solid/link.svg",
        "wagtailfontawesomesvg/solid/list.svg",
        "wagtailfontawesomesvg/solid/map-marker.svg",
        "wagtailfontawesomesvg/solid/medkit.svg",
        "wagtailfontawesomesvg/solid/minus.svg",
        "wagtailfontawesomesvg/solid/th.svg",
    ]


@hooks.register("construct_whitelister_element_rules")
def whitelister_element_rules():
    return {
        "h2": attribute_rule({"style": True}),
        "h3": attribute_rule({"style": True}),
        "h4": attribute_rule({"style": True}),
        "h5": attribute_rule({"style": True}),
        "p": attribute_rule({"style": True}),
    }


class MessageAdmin(OrderableMixin, ModelAdmin):
    model = Message
    menu_label = "Messages"
    menu_icon = "pilcrow"
    menu_order = 1000  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = True
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


modeladmin_register(MessageAdmin)
