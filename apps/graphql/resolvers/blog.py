from typing import Any

from graphql import GraphQLResolveInfo

from apps.blog.models import BlogPage, BlogCategory


def resolve_blogpages(obj: Any, info: GraphQLResolveInfo, category=None):
    blogpages = BlogPage.objects.live().order_by("-date", "-id")
    bp_list = []
    for bp in blogpages:
        bp_list += [bp.get_dict("fill-300x150|jpegquality-60")]

    return bp_list


def resolve_blogpage(obj: Any, info: GraphQLResolveInfo, id):
    return BlogPage.objects.get(id=id).get_dict("max-900x900")


def resolve_blogcategories(obj: Any, info: GraphQLResolveInfo):
    return BlogCategory.objects.all()
