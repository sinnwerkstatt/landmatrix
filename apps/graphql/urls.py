from django.urls import path

from .schema import schema
from .views import GraphQLGETView

urlpatterns = [
    # path("", cache_page(60 * 15)(GraphQLGETView.as_view(schema=schema)), name="graphql"),
    path("", GraphQLGETView.as_view(schema=schema), name="graphql"),
]
