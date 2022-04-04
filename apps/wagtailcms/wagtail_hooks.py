from django.conf import settings
from django.templatetags.static import static
from django.utils.html import escape, format_html, format_html_join
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.core import hooks
from wagtail.core.models import Page
from wagtail.core.rich_text.pages import PageLinkHandler
from wagtail.core.whitelist import attribute_rule
from wagtailorderable.modeladmin.mixins import OrderableMixin

from apps.message.models import Message


@hooks.register("insert_editor_js")
def editor_js():
    return """
        <script>
          registerHalloPlugin('hallojustify');
          $(function () {
            const region_dd = document.querySelector(".region-or-country #id_region");
            const country_dd = document.querySelector(".region-or-country #id_country");

            if(region_dd && country_dd) {
              region_dd.addEventListener("change", (event) => {
                if (event.target.value) country_dd.value = "";
              });
              country_dd.addEventListener("change", (event) => {
                if (event.target.value) region_dd.value = "";
              });
            }
          });
        </script>
        """


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


# GND replace link-handler with legacy-aware handler for now.
class MyPageLinkHandler(PageLinkHandler):
    @classmethod
    def expand_db_attributes(cls, attrs):
        try:
            page = cls.get_instance(attrs)

            page_url = escape(page.specific.url)
            page_url = page_url.replace("/legacy/", "/")

            return f'<a href="{page_url}">'
        except Page.DoesNotExist:
            return "<a>"


@hooks.register("register_rich_text_features", order=1)
def legacy_url_rewrite_for_richtext_to_html_parsing(features):
    features.register_link_type(MyPageLinkHandler)
