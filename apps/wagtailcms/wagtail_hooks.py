from django.utils.html import format_html
from wagtail import hooks
from wagtail.admin.viewsets.model import ModelViewSet
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


@hooks.register("insert_global_admin_js", order=100)
def monkeypatch_wagtail_modeltranslation():
    return format_html(
        '<script src="{}"></script>',
        "/static/js/cleanForSlug.js",
    )


class PartnerViewSet(ModelViewSet):
    model = Partner
    add_to_settings_menu = True
    exclude_form_fields = []
    list_display = ["name", "homepage"]
    search_fields = ["name", "homepage"]
    icon = "user"


partner_viewset = PartnerViewSet("partner")

@hooks.register("register_admin_viewset")
def register_viewset():
    return partner_viewset
