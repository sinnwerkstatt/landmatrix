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

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin

from api import urls as api_urls
from global_app import urls as global_urls
from global_app.views.filter_widget_ajax_view import FilterWidgetAjaxView
from chart_view import urls as chart_urls
from editor import urls as editor_urls


urlpatterns = i18n_patterns('',
    url('^accounts/', include('django.contrib.auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(api_urls)),
    url(r'^global_app/', include(global_urls)),
    url(r'^editor/', include(editor_urls)),
    url(r'^ajax/widget/(?P<action>operators|values)', FilterWidgetAjaxView.as_view(), name='ajax_widget'),
    url(r'^chart_view/', include(chart_urls)),
    url(r'^', include('cms.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
