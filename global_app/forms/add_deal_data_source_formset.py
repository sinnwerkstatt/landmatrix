__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from global_app.forms.deal_data_source_form import DealDataSourceForm

from django.forms.models import formset_factory
from django.template.defaultfilters import slugify
from django.core.files.storage import default_storage
from django.conf import settings
from django.core.files.base import ContentFile
from django.contrib import messages

if False:
    import urllib2
    from wkhtmltopdf import wkhtmltopdf

import os
import re


DealDataSourceBaseFormSet = formset_factory(DealDataSourceForm, extra=1)
class AddDealDataSourceFormSet(DealDataSourceBaseFormSet):
    def get_taggroups(self, request=None):
        ds_taggroups = []
        for i, form in enumerate(self.forms):
            for j, taggroup in enumerate(form.get_taggroups()):
                taggroup["main_tag"]["value"] += "_" + str(i+1)
                ds_taggroups.append(taggroup)
                ds_url, ds_file = None, None
                for t in taggroup["tags"]:
                    if t["key"] == "url":
                        ds_url = t["value"]
                    elif t["key"] == "file":
                        ds_file = t["value"]
                #if ds_file:
                #    taggroup["tags"].append({
                #            "key": "file",
                #            "value": ds_file,
                #        })
                if ds_url:
                    url_slug = "%s.pdf" % re.sub(r"http|https|ftp|www|", "", slugify(ds_url))
                    if not ds_file or url_slug != ds_file:
                        # Remove file from taggroup
                        taggroup["tags"] = filter(lambda o: o["key"] != "file", taggroup["tags"])
                        # Create file for URL
                        if not default_storage.exists("%s/%s/%s" % (os.path.join(settings.MEDIA_ROOT), "uploads", url_slug)):
                            try:
                                # Check if URL changed and no file given
                                if ds_url.endswith(".pdf"):
                                    response = urllib2.urlopen(ds_url)
                                    default_storage.save("%s/%s/%s" % (os.path.join(settings.MEDIA_ROOT), "uploads", url_slug), ContentFile(response.read()))
                                else:
                                    # Create PDF from URL
                                    wkhtmltopdf(ds_url, "%s/%s/%s" % (os.path.join(settings.MEDIA_ROOT), "uploads", url_slug))
                                # Set file tag
                            except:
                                # skip possible html to pdf conversion errors
                                if request and not default_storage.exists("%s/%s/%s" % (os.path.join(settings.MEDIA_ROOT), "uploads", url_slug)):
                                    messages.error(request, "Data source <a target='_blank' href='%s'>URL</a> could not be uploaded as a PDF file. Please upload manually." % ds_url)
                        taggroup["tags"].append({
                            "key": "file",
                            "value": url_slug,
                        })
                        # always add url, cause there is a problem with storing the file when deal get changed again
                        #taggroup["tags"].append({
                        #    "key": "url",
                        #    "value": ds_url,
                        #})
        return ds_taggroups

    @classmethod
    def get_data(cls, activity):
        taggroups = activity.a_tag_group_set.filter(fk_a_tag__fk_a_value__value__contains="data_source").order_by("fk_a_tag__fk_a_value__value")
        data = []
        for i, taggroup in enumerate(taggroups):
            data.append(DealDataSourceForm.get_data(activity, tg=taggroup))
        return data
