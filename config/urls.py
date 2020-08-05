from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django_prometheus import exports
from django_registration.backends.activation.views import RegistrationView

from apps.grid.views.deal_comparison import DealComparisonView
from apps.grid.views.filter import FilterWidgetAjaxView
from apps.grid.views.investor_comparison import InvestorComparisonView
from apps.landmatrix.forms import CustomRegistrationForm
from apps.landmatrix.views import CountryView, RegionView, SwitchLanguageView
from apps.wagtailcms.api import api_router

handler500 = "apps.landmatrix.views.handler500"

CACHE_TIMEOUT = 24 * 3600

urlpatterns = [
    path("", include("apps.landmatrix.urls")),
    path(
        "accounts/register/",
        RegistrationView.as_view(form_class=CustomRegistrationForm),
        name="registration_register",
    ),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("django_registration.backends.activation.urls")),
    path("admin/", admin.site.urls),
    path("impersonate/", include("impersonate.urls")),
    path("language/<language>/", SwitchLanguageView.as_view(), name="switch_language"),
    # Wagtail
    path("cms/", include("wagtail.admin.urls")),
    path("news/", include("blog.urls", namespace="news")),
    path("documents/", include("wagtail.documents.urls")),
    path("data/", include("apps.grid.urls")),
    path("map/", include("apps.map.urls")),
    path("charts/", include("apps.charts.urls")),
    path("deal/comments/", include("apps.public_comments.urls")),
    path("deal/", include("apps.grid.urls.deal")),
    path(
        "compare/<int:activity_1>/<int:activity_2>/",
        DealComparisonView.as_view(),
        name="compare_deals",
    ),
    path(
        "compare/<int:activity_1>/", DealComparisonView.as_view(), name="compare_deals"
    ),
    path("region/<slug:region_slug>/", RegionView.as_view(), name="region"),
    path("country/<slug:country_slug>/", CountryView.as_view(), name="country"),
    path("investor/", include("apps.grid.urls.investor")),
    path(
        "investors/compare/<int:investor_1>/<int:investor_2>/",
        InvestorComparisonView.as_view(),
        name="compare_investors",
    ),
    path(
        "investors/compare/<int:investor_1>/",
        InvestorComparisonView.as_view(),
        name="compare_investors",
    ),
    path("editor/", include("apps.editor.urls")),
    path(
        "prometheus/metrics/",
        exports.ExportToDjangoView,
        name="prometheus-django-metrics",
    ),
    path("graphql/", include("apps.graphql.urls")),
    path("wagtailapi/v2/", api_router.urls),
    # path("api/", include("apps.landmatrix.urlsapi")),
]

if settings.DEBUG:
    # Non i18n patterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    try:
        # noinspection PyUnresolvedReferences
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
    except ImportError:
        pass

urlpatterns += [
    # path('api/docs/', include('rest_framework_docs.urls')),
    path("api/", include("apps.api.urls")),
    path(
        "ajax/widget/<di:doc_type>/", FilterWidgetAjaxView.as_view(), name="ajax_widget"
    ),
    path("", include("wagtail.core.urls")),
]
