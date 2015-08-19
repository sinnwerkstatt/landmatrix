from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from djangocms_text_ckeditor.forms import TextForm
from djangocms_text_ckeditor.utils import plugin_tags_to_user_html

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import GetTheIdea


class GetTheIdeaPlugin(CMSPluginBase):

    module = "Get the idea"
    model = GetTheIdea
    name = _("Text")
    form = TextForm
    render_template = "cms/plugins/text.html"
    change_form_template = "cms/plugins/text_plugin_change_form.html"


    def get_editor_widget(self, request, plugins):
        """ Returns the Django form Widget to be used for the text area """
        from djangocms_text_ckeditor.widgets import TextEditorWidget
        return TextEditorWidget()

    def get_form_class(self, request, plugins):
        """
        Returns a subclass of Form to be used by this plugin
        """
        # We avoid mutating the Form declared above by subclassing
        class AbstractTextPluginForm(self.form):
            pass
        widget = self.get_editor_widget(request, plugins)
        AbstractTextPluginForm.declared_fields["body"] = forms.CharField(widget=widget, required=False)
        return AbstractTextPluginForm

    def get_form(self, request, obj=None, **kwargs):
        plugins = plugin_pool.get_text_enabled_plugins(self.placeholder, self.page)
        form = self.get_form_class(request, plugins)
        kwargs['form'] = form # override standard form
        return super(GetTheIdeaPlugin, self).get_form(request, obj, **kwargs)

    def render(self, context, instance, placeholder):
        print("Howdy! I'm a "+self.__class__.__name__)
        context.update({
            'body': plugin_tags_to_user_html(instance.body, context, placeholder),
            'placeholder': placeholder,
            'object': instance
        })
        return context

    def save_model(self, request, obj, form, change):
        obj.clean_plugins()
        super(GetTheIdeaPlugin, self).save_model(request, obj, form, change)


class OverviewPlugin(GetTheIdeaPlugin):
    module = _("Get the idea")
    name = _("Overview")
    render_template = "plugins/overview.html"
    model = GetTheIdea

plugin_pool.register_plugin(OverviewPlugin)


class TransnationalDealsPlugin(GetTheIdeaPlugin):
    module = _("Get the idea")
    name = _("Transnational deals")
    render_template = "plugins/transnational-deals.html"
    model = GetTheIdea
plugin_pool.register_plugin(TransnationalDealsPlugin)


class AgriculturalProducePlugin(GetTheIdeaPlugin):
    module = _("Get the idea")
    name = _("Agricultural produce")
    render_template = "plugins/agricultural-produce.html"
    model = GetTheIdea
plugin_pool.register_plugin(AgriculturalProducePlugin)


class InvestorTargetCountriesPlugin(GetTheIdeaPlugin):
    module = _("Get the idea")
    name = _("Investor/Target countries")
    render_template = "plugins/investor-target-countries.html"
    model = GetTheIdea
plugin_pool.register_plugin(InvestorTargetCountriesPlugin)


class PerspectivePlugin(GetTheIdeaPlugin):
    module = _("Get the idea")
    name = _("Perspective")
    render_template = "plugins/perspective.html"
    model = GetTheIdea
plugin_pool.register_plugin(PerspectivePlugin)

# class SizeComparisonPlugin(GetTheIdeaPlugin):
#     module = _("Get the idea")
#     name = _("Size comparison")
#     render_template = "plugins/size-comparison.html"
#     model = GetTheIdea
#
#     def render(self, context, instance, placeholder):
#         context = super(SizeComparisonPlugin, self).render(context, instance, placeholder)
#         context["items"] = PerspectiveObject.objects.order_by("position")
#         # Get number for current object
#         context["active_item"] = None
#         active_slug = context["request"].GET.get("item", "")
#         for item in context["items"]:
#             if slugify(item.name) == active_slug:
#                 context["active_item"] = item
#         if not context["active_item"]:
#             context["active_item"] = context["items"][0]
#         return context
# plugin_pool.register_plugin(SizeComparisonPlugin)

# class IntentionPlugin(GetTheIdeaPlugin):
#     module = "Get the idea"
#     name = _("Intention of investment")
#     render_template = "plugins/intention.html"
#     model = GetTheIdea
# plugin_pool.register_plugin(IntentionPlugin)

# class TransnationalDealsWidgetPlugin(CMSPluginBase):
#     module = "Widgets"
#     name = _("Transnational deals")
#     render_template = "widgets/transnational-deals.html"
#     model = TransnationalDealsWidget
# plugin_pool.register_plugin(TransnationalDealsWidgetPlugin)
#
# class MapOfInvestmentsWidgetPlugin(CMSPluginBase):
#     module = "Widgets"
#     name = _("Map of investments")
#     render_template = "widgets/map-of-investments.html"
#     model = MapOfInvestmentsWidget
# plugin_pool.register_plugin(MapOfInvestmentsWidgetPlugin)
