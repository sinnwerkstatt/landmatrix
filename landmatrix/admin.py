from django.contrib import admin
from landmatrix.models.filter_condition import FilterCondition
from landmatrix.models.filter_preset import FilterPreset

admin.site.register(FilterPreset)
admin.site.register(FilterCondition)
