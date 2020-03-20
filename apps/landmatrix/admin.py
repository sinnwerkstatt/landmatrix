from django.contrib import admin

from apps.landmatrix import models


@admin.register(models.FilterCondition)
class FilterConditionAdmin(admin.ModelAdmin):
    pass


class FilterConditionInline(admin.TabularInline):
    model = models.FilterCondition
    extra = 0


@admin.register(models.FilterPreset)
class FilterPresetAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "group",
        "relation",
        "is_default_country",
        "is_default_global",
    ]
    inlines = [FilterConditionInline]


class FilterPresetInline(admin.TabularInline):
    model = models.FilterPreset
    extra = 0


@admin.register(models.FilterPresetGroup)
class FilterPresetGroupAdmin(admin.ModelAdmin):
    inlines = [FilterPresetInline]


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ["name", "is_target_country"]


admin.site.register(models.Region)
admin.site.register(models.Status)
admin.site.register(models.HistoricalActivity)
admin.site.register(models.ActivityAttributeGroup)
admin.site.register(models.HistoricalActivityAttribute)
admin.site.register(models.ActivityChangeset)
admin.site.register(models.ReviewDecision)
admin.site.register(models.ActivityFeedback)
admin.site.register(models.Animal)
admin.site.register(models.Mineral)


@admin.register(models.Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "slug", "fk_agricultural_produce")
    list_filter = ("fk_agricultural_produce",)


admin.site.register(models.Currency)


@admin.register(models.HistoricalInvestor)
class InvestorAdmin(admin.ModelAdmin):
    search_fields = ["investor_identifier", "name"]
