from django.urls import path

from .views import MapView

urlpatterns = [path("", MapView.as_view(), name="map")]
