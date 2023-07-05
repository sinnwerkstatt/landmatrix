from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from .models import BlogIndexPage, BlogPage


@register(BlogIndexPage)
class BlogIndexPageTR(TranslationOptions):
    pass


@register(BlogPage)
class BlogPageTR(TranslationOptions):
    # fields = ("body",)
    pass


# @register(BlogCategory)
# class BlogCategoryTR(TranslationOptions):
#     fields = ("name",)
