from wagtail.api.v2.endpoints import PagesAPIEndpoint
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.documents.api.v2.endpoints import DocumentsAPIEndpoint
from wagtail.images.api.v2.endpoints import ImagesAPIEndpoint

api_router = WagtailAPIRouter("wagtailapi")

api_router.register_endpoint("pages", PagesAPIEndpoint)
api_router.register_endpoint("images", ImagesAPIEndpoint)
api_router.register_endpoint("documents", DocumentsAPIEndpoint)
