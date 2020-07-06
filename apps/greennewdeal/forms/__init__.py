from django.db.models import Model
from django.utils.translation import gettext


class VueForm:
    model: Model = None
    sections = {}

    def get_fields(self):
        modelfields = {f.name: f for f in self.model._meta.fields}
        retsections = {}
        for sectionname, section in self.sections.items():
            retsubsections = []
            for subsection in section["subsections"]:
                retfields = []
                for field in subsection["fields"]:
                    fieldname = field if isinstance(field, str) else field["name"]
                    mfield = modelfields[fieldname]
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
                            if isinstance(choice, str):
                                choices[name] = gettext(choice)
                            elif isinstance(choice, (list, tuple)):
                                choices[gettext(name)] = {
                                    cn: gettext(cv) for (cn, cv) in choice
                                }
                        richfield["choices"] = choices
                    if mfield.help_text:
                        richfield["help_text"] = gettext(mfield.help_text)

                    if isinstance(field, dict):
                        richfield.update(field)
                    retfields += [richfield]

                retsubsections += [
                    {"name": gettext(subsection["name"]), "fields": retfields,}
                ]

            retsections[sectionname] = {
                "label": gettext(section["label"]),
                "subsections": retsubsections,
            }
        return retsections
