from django.contrib.gis.db import models
from django.contrib.gis import admin

from cms.models import CMSPlugin
from djangocms_text_ckeditor.utils import plugin_tags_to_id_list, replace_plugin_tags
from django.utils.text import Truncator
from django.utils.html import strip_tags, clean_html
from django.utils.translation import ugettext_lazy as _

class MapPluginModel(CMSPlugin):
#    image = FilerImageField()
    body = models.TextField(_("body"), blank=True, null=True)


    def _set_body_admin(self, text):
        self.body = plugin_admin_html_to_tags(text)

    def _get_body_admin(self):
        return plugin_tags_to_admin_html(self.body)

    body_for_admin = property(_get_body_admin, _set_body_admin, None,
                              """
                              body attribute, but with transformations
                              applied to allow editing in the
                              admin. Read/write.
                              """)

    search_fields = ('body',)

    def __str__(self):
        truncator = Truncator(strip_tags(self.body))
        return u"%s" % (truncator.words(3)[:30]+"...")

    def clean(self):
        self.body = clean_html(self.body)

    def clean_plugins(self):
        ids = plugin_tags_to_id_list(self.body)
        plugins = CMSPlugin.objects.filter(parent=self)
        for plugin in plugins:
            if not plugin.pk in ids:
                plugin.delete() #delete plugins that are not referenced in the text anymore

    def post_copy(self, old_instance, ziplist):
        """
        Fix references to plugins
        """

        replace_ids = {}
        for new, old in ziplist:
            replace_ids[old.pk] = new.pk

        self.body = replace_plugin_tags(old_instance.get_plugin_instance()[0].body, replace_ids)
        self.save()


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
