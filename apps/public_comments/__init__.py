"""
Public comments is a place for use to modify the behaviour of ThreadedComments
and django.contrib.comments. It is only used for comments by non moderators.
"""


def get_model():
    """
    Use the ThreadedComment model without modifications.
    """
    from .models import ThreadedComment

    return ThreadedComment


def get_form():
    """
    Replace the threaded comment form with ours.
    """
    from .forms import PublicCommentForm

    return PublicCommentForm
