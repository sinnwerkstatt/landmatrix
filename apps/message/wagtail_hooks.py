from wagtail import hooks

from .views import message_viewset


@hooks.register("register_admin_viewset")
def register_viewset():
    return message_viewset
