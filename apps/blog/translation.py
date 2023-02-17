from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from .models import BlogIndexPage, BlogPage


@register(BlogIndexPage)
class BlogIndexPageTR(TranslationOptions):
    pass


@register(BlogPage)
class BlogPageTR(TranslationOptions):
    pass


# after this run:
# ./manage.py makemigrations
# ./manage.py migrate
# ./manage.py sync_page_translation_fields
# ./manage.py update_translation_fields
#
# @register(BlogCategory)
# class BlogCategoryTR(TranslationOptions):
#     fields = ("name",)
