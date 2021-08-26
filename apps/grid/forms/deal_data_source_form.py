"""
TODO: cleanup formset_factory handling.
"""

from django import forms
from django.core.files.base import File
from django.forms.models import formset_factory
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _

from apps.grid.fields import FileFieldWithInitial, TitleField, YearMonthDateField
from apps.grid.forms.base_form import BaseForm
from apps.grid.widgets import CommentInput
from apps.landmatrix.storage import data_source_storage


class DealDataSourceForm(BaseForm):
    form_title = "Data source"
    exclude_in_export = ("file_not_public", "includes_in_country_verified_information")

    tg_data_source = TitleField(required=False, label="", initial=_("Data source"))
    type = forms.ChoiceField(
        required=False,
        label=_("Data source type"),
        choices=(
            ("", _("---------")),
            ("Media report", _("Media report")),
            ("Research Paper / Policy Report", _("Research Paper / Policy Report")),
            ("Government sources", _("Government sources")),
            ("Company sources", _("Company sources")),
            ("Contract", _("Contract")),
            (
                "Contract (contract farming agreement)",
                _("Contract (contract farming agreement)"),
            ),
            ("Personal information", _("Personal information")),
            ("Crowdsourcing", _("Crowdsourcing")),
            ("Other", _("Other (Please specify in comment field)")),
        ),
    )
    url = forms.URLField(required=False, label=_("URL"))
    file = FileFieldWithInitial(
        required=False, label=_("File"), help_text=_("Maximum file size: 10MB")
    )
    file_not_public = forms.BooleanField(required=False, label=_("Keep PDF not public"))
    publication_title = forms.CharField(required=False, label=_("Publication title"))
    date = YearMonthDateField(
        required=False,
        label=_("Date"),
        help_text="[YYYY-MM-DD]",
        #    input_formats=["%d.%m.%Y", "%d:%m:%Y", "%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"]
    )

    # Optional personal information for Crowdsourcing and Personal information
    name = forms.CharField(required=False, label=_("Name"))
    company = forms.CharField(required=False, label=_("Organisation"))
    email = forms.CharField(required=False, label=_("Email"))
    phone = forms.CharField(required=False, label=_("Phone"))
    includes_in_country_verified_information = forms.BooleanField(
        required=False, label=_("Includes in-country-verified information")
    )
    open_land_contracts_id = forms.CharField(
        required=False, label=_("Open Contracting ID")
    )
    tg_data_source_comment = forms.CharField(
        required=False, label=_("Comment on data source"), widget=CommentInput
    )

    class Meta:
        name = "data_source"

    # def clean_date(self):
    #    date = self.cleaned_data["date"]
    #    try:
    #        return date and date.strftime("%Y-%m-%d") or ""
    #    except ValueError:
    #        raise forms.ValidationError(
    #            _("Invalid date. Please enter a date in the format [YYYY-MM-DD]")
    #        )

    def clean_file(self):
        file = self.cleaned_data["file"]
        if file and isinstance(file, File):
            n = file.name.split(".")
            # cleanup special charachters in filename
            file.name = "%s.%s" % (slugify(n[0]), n[1]) if len(n) > 1 else slugify(n[0])
        return file

    def get_availability_total(self):
        return 4  # pragma: no cover

    def get_fields_display(self, user=None):
        if not (
            user
            and user.is_authenticated
            and user.has_perm("landmatrix.review_historicalactivity")
        ):
            # Remove file field if not Editor/Admin
            if self.initial.get("file_not_public", False):
                self.initial.pop("file_not_public")
                if "file" in self.initial:
                    self.initial.pop("file")
            # Remove personal information fields
            for field_name in ("name", "company", "email", "phone"):
                if field_name in self.initial:
                    self.initial.pop(field_name)
        return super().get_fields_display(user=user)

    #    #next_group_id = next_group.id if next_group else ActivityAttributeGroup.objects.order_by('pk').last().id
    #    #if hasattr(deal.activity, 'history_date'):  # isinstance(deal, DealHistoryItem):
    #    #    deal_date = deal.activity.history_date
    #    #    deal_activity = Activity.objects.get(pk=deal.activity.id).history.as_of(deal_date)
    #    #else:
    #    #    deal_activity = deal.activity
    #    #tags = ActivityAttributeGroup.objects.filter(fk_activity=deal_activity).\
    #    #    filter(pk__gte=group.id).filter(pk__lte=next_group_id).\
    #    #    filter(belongs_to_data_source).values_list('attributes', flat=True)


#
#    attributes = {}
#    for tag in tags:
#        for key in tag.keys():
#            if key in attributes and attributes[key] != tag[key]:
#                # raise RuntimeError()
#                # print(
#                #     'ALERT: found different values under the same tag group. Deal ID {}, group {}, tags {}'.format(
#                #         deal.activity.activity_identifier, group.id, str(tags)
#                #     ))
#                pass
#            attributes[key] = tag[key]
#
#    return attributes


DealDataSourceBaseFormSet = formset_factory(DealDataSourceForm, extra=0)


class AddDealDataSourceFormSet(DealDataSourceBaseFormSet):
    form_title = _("Data sources")
    extra = 1
    max_num = 1

    def get_attributes(self, request=None):
        attributes = []
        for count, form in enumerate(self.forms):
            form_attributes = form.get_attributes(request)

            # FIXME: Move this to DealDataSourceForm.get_attributes
            uploaded = self.get_file_from_upload(request.FILES, count)
            if uploaded:
                if "file" in form_attributes:
                    form_attributes["file"]["value"] = uploaded  # pragma: no cover
                else:
                    form_attributes["file"] = {"value": uploaded}

            attributes.append(form_attributes)
        return attributes

    @classmethod
    def get_data(cls, activity, group=None, prefix=""):
        groups = (
            activity.attributes.filter(fk_group__name__startswith=cls.Meta.name)
            .values_list("fk_group__name", flat=True)
            .order_by("fk_group__name")
            .distinct()
        )
        data = []
        for i, group in enumerate(groups):
            form_data = DealDataSourceForm.get_data(
                activity, group=group
            )  # , prefix='%s-%i' % (cls.Meta.name, i))
            if form_data:
                data.append(form_data)
        return data

    def get_file_from_upload(self, files, form_index):
        key = "data_source-{}-file-new".format(form_index)
        file = files.get(key)
        if file:
            return data_source_storage.save(file.name, file)
        return None

    class Meta:
        name = "data_source"


class ChangeDealDataSourceFormSet(AddDealDataSourceFormSet):
    extra = 0


class PublicViewDealDataSourceForm(DealDataSourceForm):
    class Meta:
        name = "data_source"
        fields = ("tg_data_source", "type", "url", "company", "date")
        readonly_fields = ("tg_data_source", "type", "url", "company", "date")


class PublicViewDealDataSourceFormSet(
    formset_factory(
        PublicViewDealDataSourceForm, formset=AddDealDataSourceFormSet, extra=0
    )
):
    form_title = _("Data sources")
