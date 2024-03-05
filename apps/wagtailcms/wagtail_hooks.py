from django.utils.html import format_html
from wagtail import hooks
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.whitelist import attribute_rule

from apps.wagtailcms.partners import Partner


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


class PartnerViewSet(SnippetViewSet):
    model = Partner
    add_to_admin_menu = False
    form_fields_exclude = []
    list_display = ["name", "logo", "homepage"]
    list_filter = ["name", "homepage"]
    menu_icon = "user"


register_snippet(PartnerViewSet)
