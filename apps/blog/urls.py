from django.urls import re_path

from . import views


app_name = "blog"

urlpatterns = [
    re_path(r"^tag/(?P<tag>[-\w]+)/", views.tag_view, name="tag"),
    re_path(
        r"^category/(?P<category>[-\w]+)/feed/$",
        views.LatestCategoryFeed(),
        name="category_feed",
    ),
    re_path(r"^category/(?P<category>[-\w]+)/", views.category_view, name="category"),
    re_path(r"^author/(?P<author>[-\w]+)/", views.author_view, name="author"),
    re_path(
        r"(?P<blog_slug>[\w-]+)/rss.*/",
        views.LatestEntriesFeed(),
        name="latest_entries_feed",
    ),
    re_path(
        r"(?P<blog_slug>[\w-]+)/atom.*/",
        views.LatestEntriesFeedAtom(),
        name="latest_entries_feed_atom",
    ),
]
