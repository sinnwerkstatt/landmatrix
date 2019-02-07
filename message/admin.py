from django.contrib import admin

from .models import Message


class MessageAdmin(admin.ModelAdmin):

    list_display = ('title', 'text', 'level', 'is_active')
    list_filter = ('level', 'is_active')

admin.site.register(Message, MessageAdmin)
