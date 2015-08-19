
from chart_view.models import AnimalPlugin

from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from djangocms_text_ckeditor.forms import TextForm
from djangocms_text_ckeditor.utils import plugin_tags_to_user_html

from django import forms
from django.utils.translation import ugettext_lazy as _


class CMSAnimalPlugin(CMSPluginBase):
    model = AnimalPlugin
    module = _("Get the idea")
    name = _("Animal Plugin")  # name of the plugin in the interface
    render_template = "plugins/animal.html"

    def render(self, context, instance, placeholder):
        context.update({'instance': instance})
        return context

plugin_pool.register_plugin(CMSAnimalPlugin)  # register the plugin

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
        return None
        return TextForm()

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
        print('Howdy!')
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

from pprint import pprint
pprint(plugin_pool.get_all_plugins())
pprint(plugin_pool.get_patterns())
