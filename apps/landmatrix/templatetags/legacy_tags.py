from collections import OrderedDict

from django import template
from django.utils.translation import gettext_lazy as _

register = template.Library()


@register.simple_tag
def get_user_role(user):
    output = []
    roles = OrderedDict()
    roles["Administrators"] = _("Administrator")
    roles["Editors"] = _("Editor")
    roles["Reporters"] = _("Reporter")
    groups = [g.name for g in user.groups.all()]
    for role, name in roles.items():
        if role in groups:
            output.append(str(name))
    if not output:
        output.append(str(_("No role")))
    userregionalinfo = None
    try:
        userregionalinfo = user.userregionalinfo
    except:
        pass
    if userregionalinfo:
        area = [c.name for c in user.userregionalinfo.country.all()]
        area.extend([r.name for r in user.userregionalinfo.region.all()])
        if area:
            output.append(str(_("for")))
            output.append(", ".join(area))
    return " ".join(output)
