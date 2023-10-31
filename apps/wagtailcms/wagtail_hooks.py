from wagtailorderable.modeladmin.mixins import OrderableMixin

from django.utils.html import format_html
from wagtail import hooks
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.whitelist import attribute_rule

from apps.message.models import Message


@hooks.register("register_icons")
def register_icons(icons):
    return icons + [
        "wagtailfontawesomesvg/brands/twitter.svg",
        "wagtailfontawesomesvg/solid/left-right.svg",
        "wagtailfontawesomesvg/solid/table-columns.svg",
        "wagtailfontawesomesvg/solid/flag.svg",
        "wagtailfontawesomesvg/solid/folder.svg",
        "wagtailfontawesomesvg/solid/image.svg",
        "wagtailfontawesomesvg/solid/link.svg",
        "wagtailfontawesomesvg/solid/list.svg",
        "wagtailfontawesomesvg/solid/location-dot.svg",
        "wagtailfontawesomesvg/solid/suitcase-medical.svg",
        "wagtailfontawesomesvg/solid/minus.svg",
        "wagtailfontawesomesvg/solid/table-cells-large.svg",
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


@hooks.register("insert_global_admin_js", order=100)
def monkeypatch_wagtail_modeltranslation():
    return format_html(
        '<script src="{}"></script>',
        "/static/js/cleanForSlug.js",
    )


class MessageAdmin(OrderableMixin, SnippetViewSet):
    model = Message
    menu_label = "Messages"
    icon = "pilcrow"
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


register_snippet(MessageAdmin)
