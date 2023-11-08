from wagtail.contrib.modeladmin.mixins import ThumbnailMixin

from django.utils.html import format_html
from wagtail import hooks
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
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



class PartnerAdmin(ThumbnailMixin, ModelAdmin):
    model = Partner
    list_display = ["name", "admin_thumb", "homepage"]
    search_fields = ["name", "homepage"]
    thumb_image_field_name = "logo"
    thumb_image_filter_spec = "fill-300x100"
    thumb_image_width = 200
    menu_icon = "user"
    menu_order = 203


modeladmin_register(PartnerAdmin)
