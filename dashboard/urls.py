from dashboard.views.editor_view import EditorView
from dashboard.views.manage_view import ManageView, ManageContentView
from global_app.views.add_deal_view import AddDealView

from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required, user_passes_test

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

""" For more information please see: https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

def allowed_to_manage(user):
    print('allowed_to_manage:', user)
    print(user.group_set.all())
    return True
    ("Read-only", "Research admins", "Research assistants")

urlpatterns = patterns('dashboard.views',
    url(r'^$', login_required(EditorView.as_view()), name='app_main'),
    url(
        r'^manage/(?P<type>deal|investor)/(?P<action>approve|reject)/(?P<id>[0-9]+)/',
        # user_passes_test(allowed_to_manage, ManageContentView.as_view()), name='manage_deal'
        ManageContentView.as_view(), name='manage_deal'
    ),
    url(
        r'^manage/',
        # user_passes_test(allowed_to_manage, ManageView.as_view()), name='manage'),
        ManageView.as_view(), name='manage'),
    url(r'^manage', login_required(ManageView.as_view()), name='app_main'),
)
