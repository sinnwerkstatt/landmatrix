from django.contrib import admin

from apps.landmatrix.models.country import Country, Region
from apps.landmatrix.models.currency import Currency
from apps.landmatrix.models.deal import Deal
from apps.landmatrix.models.investor import Investor, InvestorVentureInvolvement


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ["name", "high_income"]
    exclude = ["geom"]


admin.site.register(Region)
admin.site.register(Currency)


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    pass


@admin.register(Investor)
class InvestorAdmin(admin.ModelAdmin):
    list_display = ["pk", "__str__", "created_at"]


@admin.register(InvestorVentureInvolvement)
class InvestorVentureInvolvementAdmin(admin.ModelAdmin):
    list_display = ["pk", "__str__"]
