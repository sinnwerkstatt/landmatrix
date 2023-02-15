from django.utils import translation

from apps.blog.models import BlogCategory, BlogPage


def resolve_blogpages(_obj, _info, category=None):
    qs = BlogPage.objects.live()

    if category:
        qs = qs.filter(blog_categories__slug=category)

    blogpages = qs.order_by("-date", "-id")
    bp_list = []
    for bp in blogpages:
        bp_list += [bp.get_dict("fill-500x500|jpegquality-60")]

    return bp_list


# noinspection PyShadowingBuiltins
def resolve_blogpage(_obj, _info, id):
    return BlogPage.objects.get(id=id).get_dict("max-900x900")


def resolve_blogcategories(_obj, _info, language="en"):
    with translation.override(language):
        return BlogCategory.objects.all()
