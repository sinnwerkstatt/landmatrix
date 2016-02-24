__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django import forms


class CommentInput(forms.Textarea):
    def render(self, name, value, attrs={}):
        attrs.update({'rows': '3', 'class': 'form-control'})
        return super(CommentInput, self).render(name, value, attrs)
