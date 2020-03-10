from django.contrib import admin
from django.contrib.admin import TabularInline
from reversion.admin import VersionAdmin

from apps.greennewdeal.models import (
    Contract,
    DataSource,
    Deal,
    Investor,
    InvestorVentureInvolvement,
    Location,
)


class InlineLocations(TabularInline):
    model = Location
    extra = 0


class InlineContracts(TabularInline):
    model = Contract
    extra = 0


class InlineDataSources(TabularInline):
    model = DataSource
    extra = 0


@admin.register(Deal)
class DealAdmin(VersionAdmin):
    inlines = [InlineLocations, InlineContracts, InlineDataSources]


@admin.register(Location)
class LocationAdmin(VersionAdmin):
    list_display = ["pk", "__str__"]


@admin.register(DataSource)
class DataSourceAdmin(VersionAdmin):
    list_display = ["pk", "__str__"]


@admin.register(Contract)
class ContractAdmin(VersionAdmin):
    list_display = ["pk", "__str__"]


@admin.register(Investor)
class InvestorAdmin(VersionAdmin):
    list_display = ["pk", "__str__", "timestamp"]


@admin.register(InvestorVentureInvolvement)
class InvestorVentureInvolvementAdmin(VersionAdmin):
    list_display = ["pk", "__str__"]
