from mapping.map_model import MapModel
from migrate import V1, V2

from landmatrix.models.activity import Activity, HistoricalActivity
from django_comments.models import Comment
from threadedcomments.models import ThreadedComment

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class MapDjangoComments(MapModel):

    old_class = Comment
    new_class = Comment

    @classmethod
    def all_records(cls):
        return Comment.objects.using(V1).values()

    @classmethod
    def save_record(cls, new, save):
        #new.content_type_id = 24
        activity_identifier = HistoricalActivity.objects.using(V2).get(pk=new.object_pk).activity_identifier
        activity = Activity.objects.using(V2).get(activity_identifier=activity_identifier)
        #new.object_pk = activity.id
        new.content_object = activity
        if save:
            new.save(using=V2)

class MapThreadedComments(MapModel):
    old_class = ThreadedComment
    new_class = ThreadedComment
    depends = [MapDjangoComments]

    @classmethod
    def all_records(cls):
        comment_ids = list(Comment.objects.using(V2).values_list('id', flat=True))
        return ThreadedComment.objects.using(V1).filter(pk__in=comment_ids).values()

    @classmethod
    def save_record(cls, new, save):
        if save:
            new.save(using=V2, skip_tree_path=True)

