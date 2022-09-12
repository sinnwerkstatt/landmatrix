from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth import get_user_model

from apps.editor.models import UserRegionalInfo

User = get_user_model()


class UserRegionalInfoInline(admin.StackedInline):
    model = UserRegionalInfo
    can_delete = False
    verbose_name_plural = "regional info"
    fk_name = "user"


# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
class UserAdmin(ModelAdmin):
    def set_inactive(self, _request, queryset):
        queryset.update(is_active=False)

    set_inactive.short_description = "Set selected users INACTIVE"

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "last_login",
        "date_joined",
    )
    inlines = (UserRegionalInfoInline,)
    actions = [set_inactive]


# Re-register UserAdmin
# admin.site.unregister(User)
admin.site.register(User, UserAdmin)
