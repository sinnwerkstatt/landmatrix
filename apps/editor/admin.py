from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from .models import UserRegionalInfo

User = get_user_model()


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UserRegionalInfoInline(admin.StackedInline):
    model = UserRegionalInfo
    can_delete = False
    verbose_name_plural = "regional info"
    fk_name = "user"


# noinspection PyUnusedLocal
def set_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)


set_inactive.short_description = "Set selected users INACTIVE"


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "last_login",
        "date_joined",
    )
    inlines = (UserRegionalInfoInline,)
    actions = [set_inactive]


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
