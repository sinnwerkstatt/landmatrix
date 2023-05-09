from typing import Type

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import User

UserModel: Type[User] = get_user_model()


class MyUserAdmin(UserAdmin):
    def set_inactive(self, request, queryset):
        # let's exclude the requester, otherwise they will snooker themselves
        queryset.exclude(id=request.user.id).update(is_active=False)

    set_inactive.short_description = "Flag selected users as inactive"

    def set_active(self, request, queryset):
        queryset.exclude(id=request.user.id).update(is_active=True)

    set_active.short_description = "Activate selected users"

    list_display = UserAdmin.list_display + ("is_active", "role")
    list_filter = UserAdmin.list_filter + ("role",)
    fieldsets = UserAdmin.fieldsets + (
        (_("Data"), {"fields": ("role", "country", "region")}),
    )
    actions = [set_active, set_inactive]


admin.site.register(UserModel, MyUserAdmin)
