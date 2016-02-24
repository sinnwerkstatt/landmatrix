from django import template
from django.template.loader import render_to_string

from cms.models import Page

register = template.Library()


def do_show_gettheidea_menu(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, pagetitle, template_path = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])

    if not (template_path[0] == template_path[-1] and template_path[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)

    return GetTheIdeaMenuNode(pagetitle[1:-1], template_path[1:-1])


class GetTheIdeaMenuNode(template.Node):
    def __init__(self, pagetitle, template_path):
        self.template_path = template_path
        self.reverse_id = template.Variable(pagetitle)
        page_with_reverse_id = Page.objects.public().filter(title_set__title=pagetitle)
        self.node = page_with_reverse_id[0] if page_with_reverse_id else None

    def render(self, context):
        if not self.node: return ''
        try:
            nodes = []
            for n in self.node.children.public().filter(in_navigation=True):
                thumb = ""
                try:
                    thumb = n.placeholders.filter(slot="infographic")[0].get_plugins()[0].gettheidea.image
                except:
                    pass
                n.thumb = thumb
                nodes.append(n)
            if len(nodes) > 0:
                return render_to_string(self.template_path, {'nodes': nodes, 'current_page': context['current_page']})
        except template.VariableDoesNotExist:
            pass
        return ''


register.tag('show_gettheidea_menu', do_show_gettheidea_menu)


@register.filter
def subtract(value, arg):
    return value - arg
