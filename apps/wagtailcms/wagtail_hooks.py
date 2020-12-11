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
    js_files = [
        "js/observatorypage.js",
    ]
    js_includes = format_html_join(
        "\n",
        '<script src="{0}"></script>',
        ((static(filename),) for filename in js_files),
    )

    return js_includes + format_html(
        """
        <script>
          registerHalloPlugin('hallojustify');
        </script>
        """
    )


@hooks.register("insert_editor_css")
def editor_css():
    # Add extra CSS files to the admin like font-awesome
    css_files = [
        "font-awesome/css/font-awesome.min.css",
        "css/wagtail-font-awesome.css",
    ]

    css_includes = format_html_join(
        "\n",
        '<link rel="stylesheet" href="{0}{1}">',
        ((settings.STATIC_URL, filename) for filename in css_files),
    )

    return css_includes


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
            if settings.NEW_ROUTES:
                page_url = page_url.replace("/legacy/", "/")

            return f'<a href="{page_url}">'
        except Page.DoesNotExist:
            return "<a>"


@hooks.register("register_rich_text_features", order=1)
def legacy_url_rewrite_for_richtext_to_html_parsing(features):
    features.register_link_type(MyPageLinkHandler)
