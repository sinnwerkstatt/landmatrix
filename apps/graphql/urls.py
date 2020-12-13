from django.urls import path
from django.views.decorators.cache import cache_page

from .schema import schema
from .views import GraphQLGETView

CACHE_TTL = 60 * 60 * 24 * 30
urlpatterns = [
    # path(
    #     "",
    #     cache_page(CACHE_TTL, key_prefix="graphql")(
    #         GraphQLGETView.as_view(schema=schema)
    #     ),
    #     name="graphql",
    # ),
    path("", GraphQLGETView.as_view(schema=schema), name="graphql"),
]
