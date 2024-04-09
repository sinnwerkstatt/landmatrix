from django.utils.text import Truncator
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from wagtail.images.api.fields import ImageRenditionField

from apps.blog.models import BlogCategory, BlogPage


class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ["id", "name", "slug", "description"]


class ImageRenditionFieldSerializer(serializers.Serializer):
    url = serializers.CharField()
    full_url = serializers.CharField()
    width = serializers.IntegerField()
    height = serializers.IntegerField()
    alt = serializers.CharField()


@extend_schema_field(ImageRenditionFieldSerializer)
class AnnotatedImageRenditionField(ImageRenditionField):
    pass


class BlogPageSerializer(serializers.ModelSerializer):
    class BlogTagSerializer(serializers.Serializer):
        id = serializers.CharField()
        name = serializers.CharField()
        slug = serializers.CharField()

    excerpt = serializers.SerializerMethodField()
    header_image = AnnotatedImageRenditionField("fill-500x500|jpegquality-60")
    body = serializers.CharField(read_only=True)
    tags = serializers.SerializerMethodField()
    categories = BlogCategorySerializer(
        many=True, read_only=True, source="blog_categories"
    )

    class Meta:
        model = BlogPage
        fields = [
            "id",
            "title",
            "slug",
            "body",
            "excerpt",
            "date",
            "header_image",
            "tags",
            "categories",
            "url",
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_excerpt(self, obj):
        return Truncator(str(obj.body)).words(50, html=True, truncate=" …")

    @extend_schema_field(BlogTagSerializer(many=True))
    def get_tags(self, obj):
        return [
            {"id": tag.id, "name": tag.name, "slug": tag.slug} for tag in obj.tags.all()
        ]
