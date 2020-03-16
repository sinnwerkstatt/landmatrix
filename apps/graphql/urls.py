from ariadne.contrib.django.views import GraphQLView
from django.urls import path

from .schema import schema

urlpatterns = [
    path("", GraphQLView.as_view(schema=schema), name="graphql"),
]
