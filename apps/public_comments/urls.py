from django.conf.urls import include
from django.urls import path

from .views import EditCommentView

urlpatterns = [
    path('', include('django_comments.urls')),
    path('edit/<int:comment_id>/', EditCommentView.as_view(), name='comments-edit'),
]
