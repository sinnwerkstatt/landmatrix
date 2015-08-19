from cms.models import CMSPlugin
from djangocms_text_ckeditor.utils import plugin_tags_to_id_list

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import Truncator
from django.utils.html import strip_tags, clean_html


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
        self.body = clean_html(self.body)

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
