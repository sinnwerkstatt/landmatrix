from global_app.views.filter_widget_mixin import FilterWidgetMixin
from .models import MapPluginModel

from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from djangocms_text_ckeditor.forms import TextForm

from django import forms
from django.utils.translation import ugettext_lazy as _


MAX_NUM_DEALS = 500


class MapPlugin(CMSPluginBase, FilterWidgetMixin):

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
        self._set_filters(context['request'].GET)
        context.update({
            'filters': self.filters,
            'empty_form_conditions': self.current_formset_conditions
        })
        return context

    def save_model(self, request, obj, form, change):
        obj.clean_plugins()
        super().save_model(request, obj, form, change)

    def _set_filters(self, GET):
        self.current_formset_conditions = self.get_formset_conditions(self._filter_set(GET), GET, None, self.rules)
        self.filters = self.get_filter_context(self.current_formset_conditions, None, None, None, GET.get("starts_with"))

plugin_pool.register_plugin(MapPlugin)
