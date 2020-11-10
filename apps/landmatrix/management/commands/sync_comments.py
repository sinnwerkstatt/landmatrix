from django.core.management.base import BaseCommand
from django_comments.models import Comment, CommentFlag

from apps.landmatrix.models import HistoricalActivity


class Command(BaseCommand):
    def handle(self, *args, **options):
        for comm in Comment.objects.filter(content_type_id__in=[42, 56]):
            # TODO Threadedcomments!
            flags = CommentFlag.objects.filter(comment_id=comm.id)
            comm.id = None
            hact = HistoricalActivity.objects.get(id=comm.object_pk)
            comm.object_pk = hact.activity_identifier
            comm.content_type_id = 125
            comm.save()
            for flag in flags:
                print(flag)
                flag.id = None
                flag.comment_id = comm.id
                flag.save()
