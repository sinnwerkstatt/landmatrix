from django.db.models import Model
from django.utils.functional import Promise
from django.utils.translation import gettext

from .oldforms import (
    CustomRegistrationForm,
    ActivityFilterForm,
    ExportActivityForm,
    InvestorFilterForm,
)


class VueForm:
    model: Model = None
    sections = {}
    attributes = {}
    extra_display_fields = {}

    def __init__(self):
        self.modelfields = {f.name: f for f in self.model._meta.fields}
        self._attributes = self.attributes
        self._extra_display_fields = self.extra_display_fields

    def _process_field(self, mfield):
        vname = gettext(mfield.verbose_name)

        richfield = {
            "label": vname[0].capitalize() + vname[1:],
            "class": mfield.__class__.__name__,
        }
        if richfield["class"] in ["ForeignKey", "ManyToManyField"]:
            richfield["related_model"] = mfield.related_model.__name__
        if mfield.choices:
            choices = {}
            for name, choice in mfield.choices:
                if isinstance(choice, (str, Promise)):
                    choices[name] = gettext(choice)
                elif isinstance(choice, (list, tuple)):
                    choices[gettext(name)] = {cn: gettext(cv) for (cn, cv) in choice}
            richfield["choices"] = choices
        if mfield.help_text:
            richfield["help_text"] = gettext(mfield.help_text)

        if mfield.name in list(self._attributes.keys()):
            richfield.update(self._attributes[mfield.name])
        return richfield

    def get_fields(self):
        retfields = {}
        for name, mfield in self.modelfields.items():
            retfields[name] = self._process_field(mfield)
        retfields.update(self._extra_display_fields)
        return retfields

    # def get_sections(self):
    #     retsections = {}
    #     for sectionname, section in self.sections.items():
    #         retsubsections = []
    #         retfields = []
    #         for field in section.get("fields", []):
    #             retfields += [self._process_field(field)]
    #
    #         for subsection in section.get("subsections", []):
    #             subretfields = []
    #             for field in subsection["fields"]:
    #                 subretfields += [self._process_field(field)]
    #
    #             retsubsections += [
    #                 {"name": gettext(subsection["name"]), "fields": subretfields}
    #             ]
    #
    #         retsections[sectionname] = {"label": gettext(section["label"])}
    #         if retsubsections:
    #             retsections[sectionname]["subsections"] = retsubsections
    #         if retfields:
    #             retsections[sectionname]["fields"] = retfields
    #
    #     return retsections
