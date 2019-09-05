from django.conf.urls import include, url

from .views import EditCommentView

urlpatterns = [
    url('', include('django_comments.urls')),
    url('^edit/(?P<comment_id>[\d]+)/$', EditCommentView.as_view(), name='comments-edit'),
]
