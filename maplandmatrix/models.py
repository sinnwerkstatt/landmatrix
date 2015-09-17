from django.contrib.gis.db import models
from django.contrib.gis import admin


# Create your models here.
class Deals(models.Model):
	deals_ID = models.CharField("Deals_ID", max_length=50, unique=True, blank=False, null=True)
	investor = models.CharField("Investor", max_length = 200)
	target_country = models.CharField("Country of investment", max_length = 100)
	deal_size = models.IntegerField("Size in Hectare", blank=True, null=True)
# Box with several choices here :
	AGRICULTURE="Agriculture"
	CONSERVATION="Conservation"
	FORESTRY="Forestry"
	INDUSTRY="Industry"
	MINING="Mining"
	ENERGY="Energy"
	TOURISM="Tourism"
	OTHER="Other"
	land_use_choices = (
		(AGRICULTURE, "Agriculture"),
		(CONSERVATION, "Conservation"),
		(FORESTRY, "Forestry"),
		(INDUSTRY, "Industry"),
		(MINING, "Mining"),
		(ENERGY, "Energy"),
		(TOURISM, "Tourism"),
		(OTHER, "Other")
	)
	land_use = models.CharField("Intention of land use", max_length=500, choices=land_use_choices, default=AGRICULTURE)
	date_created = models.DateTimeField(auto_now = True)
	#lon = models.FloatField(blank=True, null= True)
	#lat = models.FloatField(blank=True, null= True)
	geom = models.PointField(srid=4326)
	objects = models.GeoManager()

	def __str__(self) :
		return "%s %s %s %s %s %s" % (self.deals_ID,self.investor, self.target_country, self.land_use, self.geom.x, self.geom.y)

	class Meta :
		verbose_name = u'Deal'
		verbose_name_plural = u'Deals'

# This is an auto-generated Django model module created by ogrinspect.
#class WorldBorder(models.Model):
	#fips = models.CharField(max_length=2)
	#iso2 = models.CharField(max_length=2)
	#iso3 = models.CharField(max_length=3)
	#un = models.IntegerField()
	#name = models.CharField(max_length=50)
	#area = models.IntegerField()
	#pop2005 = models.IntegerField()
	#region = models.IntegerField()
	#subregion = models.IntegerField()
	#lon = models.FloatField()
	#lat = models.FloatField()
	#geom = models.MultiPolygonField(srid=4326)
	#objects = models.GeoManager()

# Auto-generated `LayerMapping` dictionary for WorldBorder model
#worldborder_mapping = {
#	'fips' : 'FIPS',
#	'iso2' : 'ISO2',
#	'iso3' : 'ISO3',
#	'un' : 'UN',
#	'name' : 'NAME',
#	'area' : 'AREA',
#	'pop2005' : 'POP2005',
#	'region' : 'REGION',
#	'subregion' : 'SUBREGION',
#	'lon' : 'LON',
#	'lat' : 'LAT',
#	'geom' : 'MULTIPOLYGON',
#}
