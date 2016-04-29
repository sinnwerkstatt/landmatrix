from django.contrib import admin

from .models import NotificationEmail


class NotificationEmailAdmin(admin.ModelAdmin):
    list_display = ('created_on', 'sent_status', 'to', 'subject')
    list_display_links = list_display
    date_hierarchy = 'created_on'
    list_filter = ('sent_status', )
    readonly_fields = (
        'sent_exception', 'sent_status', 'created_on', 'sent_on', 'to', 'cc',
        'bcc', 'reply_to', 'subject', 'from_email', 'body_text', 'body_html',
    )

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(NotificationEmail, NotificationEmailAdmin)
