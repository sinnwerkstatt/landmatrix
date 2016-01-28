from api.query_sets.deals_query_set import DealsQuerySet
from .models import MapPluginModel

from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from djangocms_text_ckeditor.forms import TextForm

from django import forms
from django.utils.translation import ugettext_lazy as _

import requests


MAX_NUM_DEALS = 500

class MapPlugin(CMSPluginBase):

    module = "Map"
    model = MapPluginModel
    name = _("Map")
    form = TextForm
    render_template = "index.html"

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
        return super().get_form(request, obj, **kwargs)

    def render(self, context, instance, placeholder):
        #deals = requests.get('http://127.0.0.1:8000/en/api/deals.json?limit=%s' % MAX_NUM_DEALS).json()
        #print('RESPONSE: %s DEALS' % len(deals))
        #context['ActivityAttribute_list'] = deals
        return context

    def save_model(self, request, obj, form, change):
        obj.clean_plugins()
        super().save_model(request, obj, form, change)

plugin_pool.register_plugin(MapPlugin)
