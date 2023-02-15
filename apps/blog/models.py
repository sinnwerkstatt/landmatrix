import datetime

from taggit.models import Tag, TaggedItemBase

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.utils.text import Truncator
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from rest_framework.fields import ListField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    MultiFieldPanel,
    StreamFieldPanel,
)
from wagtail.api import APIField
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images import get_image_model_string
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import SourceImageIOError
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail_headless_preview.models import HeadlessPreviewMixin

from apps.wagtailcms.blocks import SIMPLE_CONTENT_BLOCKS

from .utils import unique_slugify


class BlogIndexPage(HeadlessPreviewMixin, Page):
    max_count = 1

    class Meta:
        verbose_name = "Blog index"

    @property
    def blogs(self):
        # Get list of blog pages that are descendants of this page
        blogs = BlogPage.objects.descendant_of(self).live()
        blogs = (
            blogs.order_by("-date")
            .select_related("owner")
            .prefetch_related(
                "tagged_items__tag",
                "categories",
                "categories__category",
            )
        )
        return blogs

    def get_context(
        self, request, tag=None, category=None, author=None, *args, **kwargs
    ):
        context = super(BlogIndexPage, self).get_context(request, *args, **kwargs)
        blogs = self.blogs

        if tag is None:
            tag = request.GET.get("tag")
        if tag:
            blogs = blogs.filter(tags__slug=tag)
        if category is None:  # Not coming from category_view in views.py
            if request.GET.get("category"):
                category = get_object_or_404(
                    BlogCategory, slug=request.GET.get("category")
                )
        if category:
            if not request.GET.get("category"):
                category = get_object_or_404(BlogCategory, slug=category)
            blogs = blogs.filter(categories__category__name=category)
        if author:
            if isinstance(author, str) and not author.isdigit():
                blogs = blogs.filter(author__username=author)
            else:
                blogs = blogs.filter(author_id=author)

        # Pagination
        page = request.GET.get("page")
        page_size = 10
        if hasattr(settings, "BLOG_PAGINATION_PER_PAGE"):
            page_size = settings.BLOG_PAGINATION_PER_PAGE

        paginator = None
        if page_size is not None:
            paginator = Paginator(blogs, page_size)  # Show 10 blogs per page
            try:
                blogs = paginator.page(page)
            except PageNotAnInteger:
                blogs = paginator.page(1)
            except EmptyPage:
                blogs = paginator.page(paginator.num_pages)

        context["blogs"] = blogs
        context["category"] = category
        context["tag"] = tag
        context["author"] = author
        context["paginator"] = paginator
        context = get_blog_context(context)

        return context

    subpage_types = ["blog.BlogPage"]


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=80, unique=True, verbose_name="Category Name")
    slug = models.SlugField(unique=True, max_length=80)
    parent = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        related_name="children",
        help_text="Categories, unlike tags, can have a hierarchy. You might have a "
        "Jazz category, and under that have children categories for Bebop"
        " and Big Band. Totally optional.",
        on_delete=models.CASCADE,
    )
    description = models.CharField(max_length=500, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"

    panels = [
        FieldPanel("name"),
        FieldPanel("parent"),
        FieldPanel("description"),
    ]

    def __str__(self):
        return self.name

    def clean(self):
        if self.parent:
            parent = self.parent
            if self.parent == self:
                raise ValidationError("Parent category cannot be self.")
            if parent.parent and parent.parent == self:
                raise ValidationError("Cannot have circular Parents.")

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slugify(self, self.name)
        return super().save(*args, **kwargs)


class BlogCategoryBlogPage(models.Model):
    category = models.ForeignKey(
        "BlogCategory",
        related_name="+",
        verbose_name="Category",
        on_delete=models.CASCADE,
    )

    page = ParentalKey("BlogPage", related_name="categories")
    panels = [FieldPanel("category")]


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey("BlogPage", related_name="tagged_items")


@register_snippet
class BlogTag(Tag):
    class Meta:
        proxy = True


def get_blog_context(context):
    """Get context data useful on all blog related pages"""
    context["authors"] = (
        get_user_model()
        .objects.filter(
            owned_pages__live=True, owned_pages__content_type__model="blogpage"
        )
        .annotate(Count("owned_pages"))
        .order_by("-owned_pages__count")
    )
    context["all_categories"] = BlogCategory.objects.all()
    context["root_categories"] = (
        BlogCategory.objects.filter(
            parent=None,
        )
        .prefetch_related(
            "children",
        )
        .annotate(
            blog_count=Count("blogpage"),
        )
    )
    return context


def limit_author_choices():
    """Limit choices in blog author field based on config settings"""
    LIMIT_AUTHOR_CHOICES = getattr(settings, "BLOG_LIMIT_AUTHOR_CHOICES_GROUP", None)
    if LIMIT_AUTHOR_CHOICES:
        if isinstance(LIMIT_AUTHOR_CHOICES, str):
            limit = Q(groups__name=LIMIT_AUTHOR_CHOICES)
        else:
            limit = Q()
            for s in LIMIT_AUTHOR_CHOICES:
                limit = limit | Q(groups__name=s)
        if getattr(settings, "BLOG_LIMIT_AUTHOR_CHOICES_ADMIN", False):
            limit = limit | Q(is_staff=True)
    else:
        limit = {"is_staff": True}
    return limit


class BlogPage(HeadlessPreviewMixin, Page):
    body = StreamField(SIMPLE_CONTENT_BLOCKS, verbose_name="body", blank=True)
    tags = ClusterTaggableManager(through="BlogPageTag", blank=True)
    date = models.DateField(
        "Post date",
        default=datetime.datetime.today,
        help_text="This date may be displayed on the blog post. It is not "
        "used to schedule posts to go live at a later date.",
    )
    header_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Header image",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        limit_choices_to=limit_author_choices,
        verbose_name="Author",
        on_delete=models.SET_NULL,
        related_name="author_pages",
    )

    search_fields = Page.search_fields + [
        index.SearchField("body"),
    ]
    blog_categories = ParentalManyToManyField(
        "BlogCategory", through="BlogCategoryBlogPage", blank=True
    )

    settings_panels = [
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("go_live_at"),
                        FieldPanel("expire_at"),
                    ],
                    classname="label-above",
                ),
            ],
            "Scheduled publishing",
            classname="publishing",
        ),
        FieldPanel("date"),
        FieldPanel("author"),
    ]

    def save_revision(self, *args, **kwargs):
        if not self.author:
            self.author = self.owner
        return super().save_revision(*args, **kwargs)

    def get_absolute_url(self):
        return self.url

    class Meta:
        verbose_name = "Blog page"
        verbose_name_plural = "Blog pages"

    content_panels = [
        FieldPanel("title", classname="full title"),
        MultiFieldPanel(
            [
                FieldPanel("tags"),
                FieldPanel("blog_categories"),
            ],
            heading="Tags and Categories",
        ),
        ImageChooserPanel("header_image"),
        StreamFieldPanel("body", classname="full"),
    ]

    def get_blog_index(self):
        # Find the closest ancestor which is a blog index
        return self.get_ancestors().type(BlogIndexPage).last()

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["blogs"] = self.get_blog_index().blogindexpage.blogs
        context = get_blog_context(context)
        return context

    def get_dict(self, rendition_str):
        try:
            header_image = self.header_image.get_rendition(rendition_str).url
        except (AttributeError, SourceImageIOError):
            header_image = None

        body = str(self.body)
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "body": body,
            "excerpt": Truncator(body).words(50, html=True, truncate=" …"),
            "date": self.date,
            "header_image": header_image,
            "tags": [
                {"id": tag.id, "name": tag.name, "slug": tag.slug}
                for tag in self.tags.all()
            ],
            "categories": list(self.blog_categories.all().values()),
            "url": self.get_url(),
        }

    parent_page_types = ["blog.BlogIndexPage"]

    def dict_tags(self):
        return [
            {"id": tag.id, "name": tag.name, "slug": tag.slug}
            for tag in self.tags.all()
        ]

    api_fields = [
        APIField("body"),
        APIField("tags", ListField(source="dict_tags")),
        APIField("date"),
        APIField("header_image"),
    ]
