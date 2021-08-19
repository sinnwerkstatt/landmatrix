from datetime import datetime

from ariadne import ScalarType

datetime_scalar = ScalarType("DateTime")


@datetime_scalar.serializer
def serialize_datetime(value: datetime) -> str:
    if isinstance(value, datetime):
        return value.isoformat()
    return value


geopoint_scalar = ScalarType("GeoPoint")


@geopoint_scalar.serializer
def serialize_geopoint(point):
    lng, lat = point
    return {"lat": lat, "lng": lng}
