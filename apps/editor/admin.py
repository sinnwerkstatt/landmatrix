from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import UserRegionalInfo


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UserRegionalInfoInline(admin.StackedInline):
    model = UserRegionalInfo
    can_delete = False
    verbose_name_plural = "regional info"
    fk_name = "user"


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserRegionalInfoInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
