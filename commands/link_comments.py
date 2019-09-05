#!/usr/bin/env python
from django.core.management import BaseCommand
from django.contrib.contenttypes.models import ContentType

from threadedcomments import get_model

from apps.landmatrix.models import HistoricalActivity, Activity


class Command(BaseCommand):
    help = 'Replace historical activity IDs with activity IDs within Threaded comments'

    def handle(self, *args, **options):
        ThreadedComment = get_model()
        passed, failed = 0, 0
        for comment in ThreadedComment.objects.filter(content_type_id=42):
            try:
                ha = HistoricalActivity.objects.get(id=comment.object_pk)
                a = Activity.objects.filter(activity_identifier=ha.activity_identifier).first()
                comment.content_type = ContentType.objects.get(app_label="landmatrix", model="activity")
                comment.object_pk = a.id
                comment.save()
                passed += 1
            except Activity.DoesNotExist:
                failed += 1
            except HistoricalActivity.DoesNotExist:
                failed += 1
        self.stdout.write('%i passed, %i failed' % (passed, failed))
