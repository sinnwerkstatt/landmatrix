#!/usr/bin/env python

from qgis.core import *
import simplejson as json

# Supply path to where is your qgis installed
QgsApplication.setPrefixPath("/usr", True)

# Load providers
QgsApplication.initQgis()

# Base directory to the data. The scripts assumes that the Shapefile and all
# CSV files are within the same directory
basedir = "/home/adrian/Desktop/"

vectorLayer = QgsVectorLayer("%s/landconcessions.shp" % basedir, "landconcessions", "ogr")
if not vectorLayer.isValid():
    print "Layer failed to load!"

provider = vectorLayer.dataProvider()

feature = QgsFeature()

# This dict maps the attribute names from the landmatrix input Shapefile to the
# fields defined in the global definition yaml
transformMap = {
    "global_ide": "identifier",
    "Country": "Country",
    "Main Crop": "Main Crop",
    "name_inves": "Name of Investor",
    "year_inves": "Year of Investment (agreed)",
    "project_st": "Project Status",
    "size_inves": "Size of Investment",
    "count_inve": "Country of Investor"
}

# List of attribute indexes to select
attributeIndexes = []
# Dict that maps the field index to the fields defined in the global YAML
fieldIndexMap = {}
for (i, field) in provider.fields().iteritems():
    if str(field.name()) in transformMap:
        attributeIndexes.append(i)
        fieldIndexMap[i] = transformMap[str(field.name())]

# Start data retreival: fetch geometry and all attributes for each feature
provider.select(attributeIndexes)

caps = provider.capabilities()

# Main dict to output
activityDiffObject = {}
activityDiffObject['activities'] = []

# Retreive every feature with its geometry and attributes
while provider.nextFeature(feature):

    # A dict for the current activity
    activityObject = {}
    activityObject['taggroups'] = []

    # Fetch map of attributes
    attrs = feature.attributeMap()

    # Fetch geometry
    geometry = feature.geometry().centroid()
    # Write the geometry to GeoJSON format
    if geometry.type() == QGis.Point:
        p = geometry.asPoint()
        geometryObject = {}
        geometryObject['type'] = 'Point'
        geometryObject['coordinates'] = [p.x(), p.y()]
    # Insert the geometry to the activity
    activityObject['geometry'] = geometryObject

    # Loop all attributes
    for (k, attr) in attrs.iteritems():
        # Handle the identifier differently
        if fieldIndexMap[k] == "identifier":
            activityObject['id'] = str(attr.toString())

        # Write all attributes that are not empty or None.
        # It is necessary to add the op property!
        # Each attribute is written to a separate taggroup
        elif attr.toString() != "" and attr is not None:
            #print "%s: %s" % (fieldIndexMap[k], attr.toString())

            taggroupObject = {}
            taggroupObject['tags'] = []

            # Get the value
            value = unicode(attr.toString())

            taggroupObject['tags'].append({"key": fieldIndexMap[k], "value": value, "op": "add"})
            activityObject['taggroups'].append(taggroupObject)

    # Append the activity to the main object
    activityDiffObject['activities'].append(activityObject)


print json.dumps(activityDiffObject, sort_keys=True, indent='    ')

# Exit the application
QgsApplication.exitQgis()