from django.contrib import admin

from apps.landmatrix.models.country import Country, Region
from apps.landmatrix.models.currency import Currency
from apps.landmatrix.models.new import (
    Area,
    Contract,
    DealDataSource,
    DealHull,
    DealVersion,
    Location,
)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ["name", "high_income"]
    exclude = ["geom"]


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    pass


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass


class ReadonlyInline(admin.TabularInline):
    extra = 0
    can_delete = False

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def has_add_permission(self, request, obj=None):
        return False

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(DealVersion)
class DealVersionAdmin(admin.ModelAdmin):
    model = DealVersion
    readonly_fields = [
        "operating_company",
        "parent_companies",
        "top_investors",
    ]


@admin.register(DealHull)
class DealHullAdmin(admin.ModelAdmin):
    class DealVersionInline(ReadonlyInline):
        model = DealVersion
        fields = [
            "id",
            "status",
            "created_at",
            "created_by",
            "sent_to_review_at",
            "sent_to_review_by",
            "sent_to_activation_at",
            "sent_to_activation_by",
            "activated_at",
            "activated_by",
            "contract_size",
            "intention_of_investment",
            "nature_of_deal",
            "negotiation_status",
            "fully_updated",
        ]

    readonly_fields = [
        "active_version",
        "draft_version",
        "confidential",
        "confidential_comment",
        "deleted",
        "deleted_comment",
        # "created_at",
        # "created_by",
        "fully_updated_at",
        "country",
    ]
    inlines = [DealVersionInline]


class AreaInline(admin.TabularInline):
    model = Area
    extra = 0
    can_delete = False


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    inlines = [AreaInline]


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    pass


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    pass


@admin.register(DealDataSource)
class DealDataSourceAdmin(admin.ModelAdmin):
    list_display = ["__str__", "id", "file", "date"]
