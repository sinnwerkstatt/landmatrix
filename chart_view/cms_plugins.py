from django.utils.translation import ugettext_lazy as _
from django.utils.text import Truncator
from django.utils.html import strip_tags, clean_html
from django.conf import settings
from django import forms
from django.db import models

from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from cms.models.pluginmodel import CMSPlugin
from djangocms_text_ckeditor.forms import TextForm

class GetTheIdea(CMSPlugin):
#    image = FilerImageField()
    body = models.TextField(_("body"), blank=True, null=True)


    def _set_body_admin(self, text):
        self.body = plugin_admin_html_to_tags(text)

    def _get_body_admin(self):
        return plugin_tags_to_admin_html(self.body)

    body_for_admin = property(_get_body_admin, _set_body_admin, None,
                              """
                              body attribute, but with transformations
                              applied to allow editing in the
                              admin. Read/write.
                              """)

    search_fields = ('body',)

    def __str__(self):
        truncator = Truncator(strip_tags(self.body))
        return u"%s" % (truncator.words(3)[:30]+"...")

    def clean(self):
        self.body = clean_html(self.body, full=False)

    def clean_plugins(self):
        ids = plugin_tags_to_id_list(self.body)
        plugins = CMSPlugin.objects.filter(parent=self)
        for plugin in plugins:
            if not plugin.pk in ids:
                plugin.delete() #delete plugins that are not referenced in the text anymore

    def post_copy(self, old_instance, ziplist):
        """
        Fix references to plugins
        """

        replace_ids = {}
        for new, old in ziplist:
            replace_ids[old.pk] = new.pk

        self.body = replace_plugin_tags(old_instance.get_plugin_instance()[0].body, replace_ids)
        self.save()

class GetTheIdeaPlugin(CMSPluginBase):

    module = "Get the idea"
    model = GetTheIdea
    name = _("Text")
    form = TextForm
    render_template = "cms/plugins/text.html"
    change_form_template = "cms/plugins/text_plugin_change_form.html"

    def get_editor_widget(self, request, plugins):
        """
        Returns the Django form Widget to be used for
        the text area
        """
        if USE_TINYMCE and "tinymce" in settings.INSTALLED_APPS:
            from cms.plugins.text.widgets.tinymce_widget import TinyMCEEditor
            return TinyMCEEditor(installed_plugins=plugins)
        else:
            return WYMEditor(installed_plugins=plugins)

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
    module = "Get the idea"
    name = _("Overview")
    render_template = "plugins/overview.html"
    model = GetTheIdea
plugin_pool.register_plugin(OverviewPlugin)

