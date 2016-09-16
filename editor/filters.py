'''
Filter the queryset given with any session dashboard filters.

TODO: get rid of session based filters for dashboard (move them to URL params)
and use django-filter
'''
from django.core.exceptions import ObjectDoesNotExist


def filter_activity_queryset(request, queryset):
    dashboard_filters = request.session.get('dashboard_filters', {})

    filtered_countries, filtered_regions, filtered_user = [], [], None

    try:
        user_regional_info = request.user.userregionalinfo
    except (ObjectDoesNotExist, AttributeError):
        user_regional_info = None

    if 'country' in dashboard_filters:
        filtered_countries = dashboard_filters.get('country')
    elif user_regional_info:
        filtered_countries = user_regional_info.country.all()

    if 'region' in dashboard_filters:
        filtered_regions = dashboard_filters.get('region')
    elif user_regional_info:
        filtered_regions = user_regional_info.region.all()

    if 'user' in dashboard_filters:
        filtered_user = dashboard_filters.get('user')
    elif user_regional_info:
        filtered_user = user_regional_info.super_user

    if filtered_countries:
        queryset = queryset.filter(
            changesets__fk_country__in=filtered_countries)
    if filtered_regions:
        queryset = queryset.filter(
            changesets__fk_country__fk_region__in=filtered_regions)
    if filtered_user:
        queryset = queryset.filter(changesets__fk_user__in=filtered_user)

    return queryset


def filter_managed_activities(user, queryset):
    '''
    for editors, show only activites that have been added/changed by public
    users
    '''
    user_is_editor = (
        user.has_perm('landmatrix.review_activity') and not
        user.has_perm('landmatrix.change_activity')
    )
    if user_is_editor:
        queryset = queryset.filter(history_user__groups__name='Reporters')

    return queryset
