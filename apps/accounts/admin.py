from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class MyUserAdmin(UserAdmin):
    def set_inactive(self, request, queryset):
        # let's exclude the requester, otherwise they will snooker themselves
        queryset.exclude(id=request.user.id).update(is_active=False)

    set_inactive.short_description = "Set selected users INACTIVE"

    list_display = UserAdmin.list_display + ("is_active", "level")
    list_filter = UserAdmin.list_filter + ("level",)
    fieldsets = UserAdmin.fieldsets + (
        (_("Data"), {"fields": ("level", "country", "region")}),
    )
    actions = [set_inactive]


admin.site.register(User, MyUserAdmin)
