from django.contrib import admin

from landmatrix.models import *


class FilterPresetAdmin(admin.ModelAdmin):
	list_display = ['name', 'group', 'relation', 'is_default', 'overrides_default']
admin.site.register(FilterPreset, FilterPresetAdmin)

admin.site.register(FilterPresetGroup)
admin.site.register(FilterCondition)

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
admin.site.register(Crop)
