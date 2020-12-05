from wagtail.admin.edit_handlers import RichTextFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core.fields import RichTextField
from wagtail.core.rich_text import expand_db_html


@register_setting(icon="radio-empty")
class ChartDescriptionsSettings(BaseSetting):
    web_of_transnational_deals = RichTextField()
    dynamics_overview = RichTextField()
    produce_info_map = RichTextField()

    class Meta:
        verbose_name = "Chart descriptions"

    def to_dict(self):
        return {
            "web_of_transnational_deals": expand_db_html(
                self.web_of_transnational_deals
            ),
            "dynamics_overview": expand_db_html(self.dynamics_overview),
            "produce_info_map": expand_db_html(self.produce_info_map),
        }

    panels = [
        RichTextFieldPanel("web_of_transnational_deals"),
        RichTextFieldPanel("dynamics_overview"),
        RichTextFieldPanel("produce_info_map"),
    ]
