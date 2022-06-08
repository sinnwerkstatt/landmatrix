from django.contrib import admin

from apps.landmatrix import models
from apps.landmatrix.models import Deal, Investor, InvestorVentureInvolvement


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ["name", "high_income"]
    exclude = ["geom"]


admin.site.register(models.Region)
admin.site.register(models.Currency)


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    pass


@admin.register(Investor)
class InvestorAdmin(admin.ModelAdmin):
    list_display = ["pk", "__str__", "created_at"]


@admin.register(InvestorVentureInvolvement)
class InvestorVentureInvolvementAdmin(admin.ModelAdmin):
    list_display = ["pk", "__str__"]
