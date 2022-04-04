from django.conf import settings
from django.contrib import messages
from django.utils.translation import LANGUAGE_SESSION_KEY, ugettext_lazy as _
from django.views.generic.base import RedirectView
from django.shortcuts import render


class SwitchLanguageView(RedirectView):
    permanent = False

    def get(self, request, language=None, *args, **kwargs):
        if language and language in dict(settings.LANGUAGES).keys():
            request.session[LANGUAGE_SESSION_KEY] = language
            request.session["django_language"] = language
            request.LANGUAGE_CODE = language
        else:
            messages.error(request, _('The language "%s" is not supported' % language))

        return super(SwitchLanguageView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        return self.request.GET.get("next", self.request.META.get("HTTP_REFERER", "/"))


def handler500(request):
    response = render(request, template_name="500.html")
    response.status_code = 500
    return response
