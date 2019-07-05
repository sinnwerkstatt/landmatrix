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

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.core import urls as wagtail_urls
from feeds.views import ActivityChangesFeed
from django_registration.backends.activation.views import RegistrationView

from grid.views.deal import *
from grid.views.deal_comparison import *
from grid.views.filter import FilterWidgetAjaxView
from grid.views.investor import *
from grid.views.investor_comparison import *
from grid.views.export import ExportView
from api import urls as api_urls
from grid import urls as grid_urls
from map import urls as map_urls
from charts import urls as charts_urls
from editor import urls as editor_urls
from landmatrix.views import *
from landmatrix.forms import CustomRegistrationForm


handler500 = 'landmatrix.views.handler500'

CACHE_TIMEOUT = 24*3600

urlpatterns = [
    #url(r'^accounts/register/$', RegistrationView.as_view(), name='registration_register'),
    url(r'^accounts/register/$', RegistrationView.as_view(
        form_class=CustomRegistrationForm
    ), name='registration_register'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/', include('django_registration.backends.activation.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^impersonate/', include('impersonate.urls')),

    url(r'^language/(?P<language>[^/]+)/$', SwitchLanguageView.as_view(), name='switch_language'),

    #url(r'^api/docs/', include('rest_framework_docs.urls')),
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

    url(r'^deal/(?P<deal_id>\d+)/$', DealDetailView.as_view(), name='deal_detail'),
    url(r'^deal/(?P<deal_id>\d+)/(?P<history_id>\d+)/$', DealDetailView.as_view(), name='deal_detail'),
    url(r'^deal/(?P<deal_id>\d+)\.pdf$', DealDetailView.as_view(), {'format': 'PDF'}, name='deal_detail_pdf'),
    url(r'^deal/(?P<deal_id>\d+)/(?P<history_id>\d+)\.pdf$', DealDetailView.as_view(), {'format': 'PDF'}, name='deal_detail_pdf'),
    url(r'^deal/(?P<deal_id>\d+)/changes\.rss$', ActivityChangesFeed(), name='deal_changes_feed'),
    url(r'^deal/(?P<deal_id>\d+)\.(?P<format>(csv|xml|xls))/$', ExportView.as_view(), name='export'),
    url(r'^deal/edit/(?P<deal_id>\d+)/$', DealUpdateView.as_view(), name='change_deal'),
    url(r'^deal/edit/(?P<deal_id>\d+)/(?P<history_id>\d+)/$', DealUpdateView.as_view(), name='change_deal'),
    url(r'^deal/add/$', DealCreateView.as_view(), name='add_deal'),
    url(r'^deal/delete/(?P<deal_id>\d+)/$', DealDeleteView.as_view(), name='delete_deal'),
    url(r'^deal/recover/(?P<deal_id>\d+)/$', DealRecoverView.as_view(), name='recover_deal'),

    url(r'^compare/(?P<activity_1>\d+)/(?P<activity_2>\d+)/$', DealComparisonView.as_view(), name='compare_deals'),
    url(r'^compare/(?P<activity_1>\d+)/$', DealComparisonView.as_view(), name='compare_deals'),

    url(r'^region/(?P<region_slug>[A-Za-z\-]+)/$', RegionView.as_view(), name='region'),
    url(r'^country/(?P<country_slug>[A-Za-z\-]+)/$', CountryView.as_view(), name='country'),

    url(r'^deal/comments/', include('public_comments.urls')),

    url(r'^investor/(?P<investor_id>\d*)/$', InvestorDetailView.as_view(), name='investor_detail'),
    url(r'^investor/(?P<investor_id>\d*)/(?P<history_id>\d+)/$', InvestorDetailView.as_view(), name='investor_detail'),
    url(r'^investor/add/$', InvestorCreateView.as_view(), name='investor_add'),
    url(r'^investor/delete/(?P<investor_id>\d+)/$', DeleteInvestorView.as_view(), name='investor_delete'),
    url(r'^investor/recover/(?P<investor_id>\d+)/$', RecoverInvestorView.as_view(), name='investor_recover'),
    url(r'^investor/edit/(?P<investor_id>\d+)/$', InvestorUpdateView.as_view(), name='investor_update'),
    url(r'^investor/edit/(?P<investor_id>\d*)/(?P<history_id>\d+)/$', InvestorUpdateView.as_view(), name='investor_update'),
    url(r'^investors/compare/(?P<investor_1_id>\d+)/(?P<investor_2_id>\d+)/$', InvestorComparisonView.as_view(), name='compare_investors'),
    url(r'^investors/compare/(?P<investor_1>\d+)/$', InvestorComparisonView.as_view(), name='compare_investors'),
    url(r'^editor/', include(editor_urls)),
    url(r'^ajax/widget/(?P<doc_type>deal|investor)/', FilterWidgetAjaxView.as_view(),name='ajax_widget'),

    url(r'', include(wagtail_urls)),
]
# Non i18n patterns
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
