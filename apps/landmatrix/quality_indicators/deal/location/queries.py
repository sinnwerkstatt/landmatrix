from django.db.models.expressions import Exists, OuterRef
from django.db.models.query_utils import Q

from apps.landmatrix.models.choices import AreaTypeEnum, LocationAccuracyEnum


def q_is_high_accuracy() -> Q:
    return Q(
        level_of_accuracy__in=[
            LocationAccuracyEnum.EXACT_LOCATION,
            LocationAccuracyEnum.COORDINATES,
        ]
    )


def q_is_georeferenced() -> Q:
    from apps.landmatrix.models.deal import Area

    subquery = Area.objects.filter(location=OuterRef("pk"))
    return Q(Exists(subquery))


def q_is_georeferenced_as(area_type: AreaTypeEnum) -> Q:
    from apps.landmatrix.models.deal import Area

    subquery = Area.objects.filter(
        location=OuterRef("pk"),
        type=area_type,
    )
    return Q(Exists(subquery))
