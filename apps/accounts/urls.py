from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.register),
    path("register_confirm/", views.register_confirm),
    path("login/", views.login),
    path("logout/", views.logout),
    path("password_reset/", views.password_reset),
    path("password_reset_confirm/", views.password_reset_confirm),
]
