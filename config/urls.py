from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from apps.landmatrix.views import SwitchLanguageView
from apps.wagtailcms.api import api_router

handler500 = "apps.landmatrix.views.handler500"

CACHE_TIMEOUT = 24 * 3600

urlpatterns = [
    # Django basics
    path("admin/", admin.site.urls),
    path("language/<language>/", SwitchLanguageView.as_view(), name="switch_language"),
    # Wagtail
    path("cms/", include("wagtail.admin.urls")),
    path("documents/", include("wagtail.documents.urls")),
    # APIs
    path("api/wagtail/v2/", api_router.urls),
    path("api/", include("apps.api.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    path("", include("wagtail.urls")),
]
