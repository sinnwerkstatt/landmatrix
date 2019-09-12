from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def involvements_for_current_activities(context, investor):
    return investor.involvements.for_current_activities(context['user'].is_staff)
