from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView
from django_comments.views.utils import next_redirect

from .forms import EditCommentForm
from .models import ThreadedComment


class EditCommentView(UpdateView):
    """
    Edits a comment. Form GET, action on POST. Requires "can moderate comments"
    permission.

    Templates: :template:`comments/edit.html`,
    Context:
        comment
            the flagged `comments.comment` object
        comment_form
            the edit form
    """
    form_class = EditCommentForm
    template_name = 'comments/landmatrix/edit.html'
    model = ThreadedComment
    queryset = ThreadedComment.objects.filter(site__pk=settings.SITE_ID)
    pk_url_kwarg = 'comment_id'
    context_object_name = 'comment'

    @method_decorator(permission_required('django_comments.can_moderate'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.save()
        return next_redirect(self.request, fallback='comments-edit-done', c=self.object.pk)
