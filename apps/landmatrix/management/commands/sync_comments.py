import sys

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django_comments.models import Comment, CommentFlag

from apps.landmatrix.models import HistoricalActivity, Deal


class Command(BaseCommand):
    def handle(self, *args, **options):
        ct = ContentType.objects.get(app_label="landmatrix", model="deal")
        for d in Deal.objects.all():
            hacts = HistoricalActivity.objects.filter(
                activity_identifier=d.id
            ).values_list("id", flat=True)

            comments = Comment.objects.filter(object_pk__in=list(hacts)).order_by("id")
            for comment in comments:
                print(comment.id, comment.object_pk, comment.content_type_id)
                comment.object_pk = d.id
                comment.content_type = ct
                comment.save()
