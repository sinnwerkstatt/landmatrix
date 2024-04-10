from django.utils import translation
from rest_framework import viewsets

from apps.blog.models import BlogCategory, BlogPage
from apps.blog.serializers import BlogCategorySerializer, BlogPageSerializer


class BlogCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BlogCategorySerializer
    queryset = BlogCategory.objects.all()
    permission_classes = []

    def list(self, request, *args, **kwargs):
        language = self.request.query_params.get("lang", "en")
        with translation.override(language):
            return super().list(request, *args, **kwargs)


class BlogPageViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BlogPageSerializer
    queryset = BlogPage.objects.all()

    def get_queryset(self):
        queryset = (
            BlogPage.objects.live()
            .prefetch_related("tags")
            .prefetch_related("blog_categories")
            .prefetch_related("header_image__renditions")
            .order_by("-date", "-id")
        )

        if category := self.request.query_params.get("category"):
            queryset = queryset.filter(blog_categories__slug=category)

        language = self.request.query_params.get("lang", "en")
        with translation.override(language):
            return queryset
