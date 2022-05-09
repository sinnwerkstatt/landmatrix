from django.contrib import admin

from apps.landmatrix import models
from apps.landmatrix.models import (
    Deal,
    Investor,
    InvestorVentureInvolvement,
)


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ["name", "high_income"]
    exclude = ["geom"]


admin.site.register(models.Region)
admin.site.register(models.HistoricalActivity)
admin.site.register(models.ActivityAttributeGroup)
admin.site.register(models.HistoricalActivityAttribute)
admin.site.register(models.ActivityChangeset)
admin.site.register(models.ReviewDecision)
admin.site.register(models.ActivityFeedback)
admin.site.register(models.Currency)


@admin.register(models.HistoricalInvestor)
class InvestorAdmin(admin.ModelAdmin):
    search_fields = ["investor_identifier", "name"]


# ### Green New Deal ### #
@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    pass


@admin.register(Investor)
class InvestorAdmin(admin.ModelAdmin):
    list_display = ["pk", "__str__", "created_at"]


@admin.register(InvestorVentureInvolvement)
class InvestorVentureInvolvementAdmin(admin.ModelAdmin):
    list_display = ["pk", "__str__"]
