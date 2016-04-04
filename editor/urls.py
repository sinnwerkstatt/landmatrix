from editor.views.editor_view import EditorView
from editor.views.manage_view import ManageView, ManageContentView
from grid.views.add_deal_view import AddDealView

from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required, user_passes_test

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


def allowed_to_manage(user):
    return bool(set(user.groups.values_list('name',flat=True)) & {"Read-only", "Research admins", "Research assistants"})


urlpatterns = patterns('editor.views',
    url(r'^$', login_required(EditorView.as_view()), name='editor'),
    url(
        r'^manage/(?P<type>deal|investor)/(?P<action>approve|reject)/(?P<id>[0-9]+)/',
        user_passes_test(allowed_to_manage)(ManageContentView.as_view()), name='manage_deal'
    ),
    url(
        r'^manage/',
        user_passes_test(allowed_to_manage)(ManageView.as_view()), name='manage'
    ),
)
