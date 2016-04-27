from mapping.map_model import MapModel
import landmatrix.models
import old_editor.models

from django_comments.models import Comment
from threadedcomments.models import ThreadedComment

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class MapCurrency(MapModel):
    old_class = old_editor.models.Currency
    new_class = landmatrix.models.Currency



