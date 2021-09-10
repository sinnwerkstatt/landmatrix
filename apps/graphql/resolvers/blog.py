from typing import Any

from django.utils import translation
from graphql import GraphQLResolveInfo

from apps.blog.models import BlogPage, BlogCategory


def resolve_blogpages(obj: Any, info: GraphQLResolveInfo, category=None):
    qs = BlogPage.objects.live()

    if category:
        qs = qs.filter(blog_categories__slug=category)

    blogpages = qs.order_by("-date", "-id")
    bp_list = []
    for bp in blogpages:
        bp_list += [bp.get_dict("fill-500x500|jpegquality-60")]

    return bp_list


def resolve_blogpage(obj: Any, info: GraphQLResolveInfo, id):
    return BlogPage.objects.get(id=id).get_dict("max-900x900")


def resolve_blogcategories(obj: Any, info: GraphQLResolveInfo, language="en"):
    with translation.override(language):
        return BlogCategory.objects.all()
