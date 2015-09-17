from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from djangocms_text_ckeditor.forms import TextForm
from djangocms_text_ckeditor.utils import plugin_tags_to_user_html

from django import forms
from django.utils.translation import ugettext_lazy as _
import random
from landmatrix.models.activity_attribute_group import ActivityAttributeGroup

from .models import MapPluginModel


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
        print("Howdy! I'm a "+self.__class__.__name__)
        # context.update({
        #     'body': plugin_tags_to_user_html(instance.body, context, placeholder),
        #     'placeholder': placeholder,
        #     'object': instance
        # })
        deal_list = []
        location_attributes = sorted(ActivityAttributeGroup.objects.filter(attributes__icontains="point_lat").
			exclude(attributes__icontains="°").\
			exclude(attributes__icontains="04.738 N").\
			exclude(attributes__icontains="-3.0001328124999426666666cro").\
			exclude(attributes__icontains="4.134665") \
                                     [:200], key=lambda x: random.random())

        for location in location_attributes:
            intention_attributes = ActivityAttributeGroup.objects.filter(attributes__icontains="intention", fk_activity_id=location.fk_activity_id)
            deal = {
			    "deal_id": location.fk_activity_id,
				"point_lat": location.attributes.get("point_lat"),
				"point_lon": location.attributes.get("point_lon"),
				"intention": intention_attributes and intention_attributes[0].attributes.get("intention") or "",
			}
            deal_list.append(deal)
        print(deal_list)
        context['ActivityAttribute_list'] = deal_list
        return context

    def save_model(self, request, obj, form, change):
        obj.clean_plugins()
        super().save_model(request, obj, form, change)

plugin_pool.register_plugin(MapPlugin)
