from django.conf.urls import url

from api.decorators import save_filter_query_params
from grid.views.all_deals_view import AllDealsView
from grid.views.export_view import ExportView
from grid.views.table_group_view import TableGroupView


CACHE_TIMEOUT = 24*3600

urlpatterns = [
    # please leave them here, commented out, for quick cache de-/activation when developing
    # url(r'^$', AllDealsView.as_view(), name='app_main'),
    # url(r'^(?P<group>.+)/(?P<list>.+)/$', TableGroupView.as_view(), name='table_list'),

    url(
        r'^$',
        save_filter_query_params()(AllDealsView.as_view()),
        name='data'
    ),
    url(
        r'^all\.(?P<format>(csv|xml|xls))/$',
        save_filter_query_params()(ExportView.as_view()),
        name='export'
    ),
    url(
        r'^(?P<group>.+)/(?P<group_value>.+)\.(?P<format>(csv|xml|xls))/$',
        save_filter_query_params()(ExportView.as_view()),
        name='export'
    ),
    url(
        r'^(?P<group>.+)\.(?P<format>(csv|xml|xls))/$',
        save_filter_query_params()(ExportView.as_view()),
        name='export'
    ),

    # needs to come last, regexp catches all expressions
    url(
        r'^(?P<group>.+)/(?P<group_value>.+)/$',
        save_filter_query_params()(TableGroupView.as_view()),
        name='table_list'
    ),
    url(
        r'^(?P<group>.+)/$',
        save_filter_query_params()(TableGroupView.as_view()),
        name='table_list'
    ),
]
