from django.contrib.gis import admin
from .models import Deals

admin.site.register(Deals, admin.OSMGeoAdmin)


# Register your models here.
