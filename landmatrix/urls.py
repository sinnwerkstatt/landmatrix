"""landmatrix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailcore import urls as wagtail_urls
from feeds.views import ActivityChangesFeed
from registration.backends.hmac.views import RegistrationView

from grid.views.change_deal_view import ChangeDealView
from grid.views.deal_comparison_view import DealComparisonView
from grid.views.deal_detail_view import DealDetailView
from grid.views.filter_widget_ajax_view import FilterWidgetAjaxView
from grid.views.stakeholder_view import AddStakeholderView, ChangeStakeholderView
from grid.views.investor_comparison_view import InvestorComparisonView
from grid.views.delete_deal_view import DeleteDealView, RecoverDealView
from grid.views.export_view import ExportView
from grid.views.add_deal_view import AddDealView
from api import urls as api_urls
from grid import urls as grid_urls
from map import urls as map_urls
from charts import urls as charts_urls
from editor import urls as editor_urls
from landmatrix.views import *
from landmatrix.forms import CustomRegistrationForm


CACHE_TIMEOUT = 24*3600

urlpatterns = [
    #url(r'^accounts/register/$', RegistrationView.as_view(), name='registration_register'),
    url(r'^accounts/register/$', RegistrationView.as_view(
        form_class=CustomRegistrationForm
    ), name='registration_register'),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^impersonate/', include('impersonate.urls')),

    url(r'^language/(?P<language>[^/]+)/$', SwitchLanguageView.as_view(), name='switch_language'),

    url(r'^api/docs/', include('rest_framework_docs.urls')),
    url(r'^api/', include(api_urls)),

    # Wagtail
    url(r'^cms/', include(wagtailadmin_urls)),
    url(r'^news/', include('blog.urls', namespace='news')),
    url(r'^documents/', include(wagtaildocs_urls)),


    #url(r'^global/', GlobalView.as_view(), name='global'),

    url(r'^data/', include(grid_urls)),
    url(r'^map/', include(map_urls)),
    url(r'^charts/', include(charts_urls)),

    # url(r'^region/(?P<region_slug>)/data/', include(grid_urls)),
    # url(r'^region/(?P<region_slug>)/map/', include(map_urls)),
    # url(r'^region/(?P<region_slug>)/charts/', include(charts_urls)),
    #
    # url(r'^country/(?P<country_slug>)/data/', include(grid_urls)),
    # url(r'^country/(?P<country_slug>)/map/', include(map_urls)),
    # url(r'^country/(?P<country_slug>)/charts/', include(charts_urls)),

    url(
        r'^deal/(?P<deal_id>\d+)/$',
        DealDetailView.as_view(),
        name='deal_detail'
    ),
    url(
        r'^deal/(?P<deal_id>\d+)/(?P<history_id>\d+)/$',
        DealDetailView.as_view(),
        name='deal_detail'
    ),
    url(
        r'^deal/(?P<deal_id>\d+)\.pdf$',
        DealDetailView.as_view(),
        {'format': 'PDF'},
        name='deal_detail_pdf'
    ),
    url(
        r'^deal/(?P<deal_id>\d+)/(?P<history_id>\d+)\.pdf$',
        DealDetailView.as_view(),
        {'format': 'PDF'},
        name='deal_detail_pdf'
    ),
    url(
        r'^deal/(?P<deal_id>\d+)/changes\.rss$',
        ActivityChangesFeed(),
        name='deal_changes_feed'
    ),
    url(
        r'^deal/(?P<deal_id>\d+)\.(?P<format>(csv|xml|xls))/$',
        ExportView.as_view(),
        name='export'
    ),

    url(
        r'^deal/edit/(?P<deal_id>\d+)/$',
        ChangeDealView.as_view(),
        name='change_deal'
    ),

    url(
        r'^deal/edit/(?P<deal_id>\d+)/(?P<history_id>\d+)/$',
        ChangeDealView.as_view(),
        name='change_deal'
    ),

    url(
        r'^deal/add/$',
        AddDealView.as_view(),
        name='add_deal'
    ),

    url(
        r'^deal/delete/(?P<deal_id>\d+)/$',
        DeleteDealView.as_view(),
        name='delete_deal'
    ),

    url(
        r'^deal/recover/(?P<deal_id>\d+)/$',
        RecoverDealView.as_view(),
        name='recover_deal'
    ),

    url(
        r'^compare/(?P<activity_1>\d+)/(?P<activity_2>\d+)/$',
        DealComparisonView.as_view(),
        name='compare_deals'
    ),
    url(
        r'^compare/(?P<activity_1>\d+)/$',
        DealComparisonView.as_view(),
        name='compare_deals'
    ),


    url(r'^region/(?P<region_slug>[A-Za-z\-]+)/$', RegionView.as_view(), name='region'),
    url(r'^country/(?P<country_slug>[A-Za-z\-]+)/$', CountryView.as_view(), name='country'),

    url(r'^deal/comments/', include('public_comments.urls')),

    url(r'^stakeholder/add/$', AddStakeholderView.as_view(), name='add_stakeholder_form'),
    url(
        r'^stakeholder/(?P<investor_id>\d+)/$',
        ChangeStakeholderView.as_view(),
        name='stakeholder_form'
    ),
    url(
        r'^stakeholder/(?P<investor_id>\d*)/(?P<history_id>\d+)/$',
        ChangeStakeholderView.as_view(),
        name='stakeholder_form'
    ),
    url(
        r'^stakeholders/compare/(?P<investor_1_id>\d+)/(?P<investor_2_id>\d+)/$',
        InvestorComparisonView.as_view(),
        name='compare_investors'
    ),
    url(
        r'^stakeholders/compare/(?P<investor_1>\d+)/$',
        InvestorComparisonView.as_view(),
        name='compare_investors'
    ),

    url(r'^editor/', include(editor_urls)),
    #url(r'^filters$', FilterView.as_view(), name='filterdebug'),
    url(r'', include(wagtail_urls)),
]
# Non i18n patterns
urlpatterns += [
    url(r'^ajax/widget/(?P<action>operators|values)', FilterWidgetAjaxView.as_view(),
            name='ajax_widget'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
