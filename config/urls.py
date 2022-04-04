from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django_registration.backends.activation.views import RegistrationView

from apps.api.views import vuebase
from apps.landmatrix.forms import CustomRegistrationForm
from apps.landmatrix.views import SwitchLanguageView
from apps.wagtailcms.api import api_router

handler500 = "apps.landmatrix.views.handler500"

CACHE_TIMEOUT = 24 * 3600

urlpatterns = [
    # Django basics
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
    path("documents/", include("wagtail.documents.urls")),
    # APIs
    path("graphql/", include("apps.graphql.urls")),
    path("wagtailapi/v2/", api_router.urls),
    path("api/", include("apps.api.urls")),
]

if settings.DEBUG:
    # Non i18n patterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    re_path(r"^(?P<path>.*)/$", vuebase),
    path("", vuebase),
    path("", include("wagtail.core.urls")),
]
