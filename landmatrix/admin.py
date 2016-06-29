from django.contrib import admin

from landmatrix.models import *

admin.site.register(FilterPreset)
admin.site.register(FilterPresetGroup)
admin.site.register(FilterCondition)
admin.site.register(Country)
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
