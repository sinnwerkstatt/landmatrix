from mapping.map_model import MapModel
import landmatrix.models
import old_editor.models
from migrate import V1, V2

from django.db import models, transaction
from django_comments.models import Comment

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class MapDjangoComments(MapModel):

    old_class = Comment
    new_class = Comment

    @classmethod
    def all_records(cls):
        return Comment.objects.using(V1).filter(is_public=True).filter(is_removed=False).values()


class MapThreadedComments(MapModel):
    pass
