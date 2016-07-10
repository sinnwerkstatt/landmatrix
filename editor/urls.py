from editor.views import *
from grid.views.add_deal_view import AddDealView

from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

urlpatterns = patterns('editor.views',
    url(r'^$',
        login_required(EditorView.as_view()),
        name='editor'),
    url(
        r'^manage/(?P<type>deal|investor)/(?P<action>approve|reject)/(?P<id>[0-9]+)/',
        login_required(ManageContentView.as_view()),
        name='manage_deal'
    ),
    url(
        r'^manage/',
        login_required(ManageView.as_view()),
        name='manage'
    ),
    url(
        r'^log/(?P<action>updates|deletes|inserts)/',
        login_required(LogView.as_view()),
        name='log'
    ),
)
