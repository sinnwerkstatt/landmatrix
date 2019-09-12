from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

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
    actions = ['resend_failed_emails']

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def resend_failed_emails(self, request, queryset):
        # Exclude already sent ones
        queryset = queryset.exclude(sent_status=NotificationEmail.STATUS_SENT)
        for email in queryset:
            email.send()
    resend_failed_emails.short_description = _("Retry failed notifications")


admin.site.register(NotificationEmail, NotificationEmailAdmin)
