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

    def __init__(self):
        self.modelfields = {f.name: f for f in self.model._meta.fields}

    def _process_field(self, field):
        fieldname = field if isinstance(field, str) else field["name"]
        mfield = self.modelfields[fieldname]
        vname = gettext(mfield.verbose_name)

        richfield = {
            "name": fieldname,
            "label": vname[0].capitalize() + vname[1:],
            "class": mfield.__class__.__name__,
        }
        if richfield["class"] == "ForeignKey":
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

        if isinstance(field, dict):
            richfield.update(field)
        return richfield

    def get_fields(self):
        retsections = {}
        for sectionname, section in self.sections.items():
            retsubsections = []
            retfields = []
            for field in section.get("fields", []):
                retfields += [self._process_field(field)]

            for subsection in section.get("subsections", []):
                subretfields = []
                for field in subsection["fields"]:
                    subretfields += [self._process_field(field)]

                retsubsections += [
                    {"name": gettext(subsection["name"]), "fields": subretfields}
                ]

            retsections[sectionname] = {"label": gettext(section["label"])}
            if retsubsections:
                retsections[sectionname]["subsections"] = retsubsections
            if retfields:
                retsections[sectionname]["fields"] = retfields

        return retsections
