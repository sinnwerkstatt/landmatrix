from ariadne import ScalarType

geopoint_scalar = ScalarType("GeoPoint")


@geopoint_scalar.serializer
def serialize_geopoint(point):
    lng, lat = point
    return {"lat": lat, "lng": lng}
