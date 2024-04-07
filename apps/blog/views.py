from rest_framework import viewsets

from apps.blog.models import BlogCategory
from apps.blog.serializers import BlogCategorySerializer


class BlogCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BlogCategorySerializer
    queryset = BlogCategory.objects.all()
    permission_classes = []
