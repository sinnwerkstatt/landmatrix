from django.contrib import admin

from landmatrix.models import *


class FilterConditionAdmin(admin.ModelAdmin):
    pass
admin.site.register(FilterCondition, FilterConditionAdmin)


class FilterConditionInline(admin.TabularInline):
    model = FilterCondition
    extra = 0


class FilterPresetAdmin(admin.ModelAdmin):
    list_display = ['name', 'group', 'relation', 'is_default_country', 'is_default_global']
    inlines = [
        FilterConditionInline
    ]
admin.site.register(FilterPreset, FilterPresetAdmin)


class FilterPresetInline(admin.TabularInline):
    model = FilterPreset
    extra = 0


class FilterPresetGroupAdmin(admin.ModelAdmin):
    inlines = [
        FilterPresetInline
    ]
admin.site.register(FilterPresetGroup, FilterPresetGroupAdmin)


class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_target_country']
admin.site.register(Country, CountryAdmin)

admin.site.register(Region)
admin.site.register(Status)
admin.site.register(Activity)
admin.site.register(HistoricalActivity)
admin.site.register(ActivityAttributeGroup)
admin.site.register(ActivityAttribute)
admin.site.register(HistoricalActivityAttribute)
admin.site.register(ActivityChangeset)
admin.site.register(ReviewDecision)
admin.site.register(ActivityFeedback)
admin.site.register(Animal)
admin.site.register(Mineral)

class CropAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'slug', 'fk_agricultural_produce')
    list_filter = ('fk_agricultural_produce',)
admin.site.register(Crop, CropAdmin)

admin.site.register(Currency)
admin.site.register(Investor)
admin.site.register(InvestorActivityInvolvement)
admin.site.register(InvestorVentureInvolvement)


