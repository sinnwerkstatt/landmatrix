from django.db.models import QuerySet
from django.db.models.aggregates import Count
from django.db.models.expressions import Exists, F
from django.db.models.query_utils import Q


def _q_any(queryset: QuerySet, q_filter: Q = Q()) -> Q:
    return Q(Exists(queryset.filter(q_filter)))


def _q_all(queryset: QuerySet, q_filter: Q = Q()) -> Q:
    return Q(
        Exists(
            queryset.annotate(
                total=Count("pk", distinct=True),
                count=Count("pk", filter=q_filter, distinct=True),
            ).filter(count=F("total"))
        )
    )


def _q_multiple(queryset: QuerySet, q_filter: Q = Q()) -> Q:
    return Q(
        Exists(
            queryset.annotate(
                count=Count("pk", filter=q_filter, distinct=True),
            ).filter(count__gt=1)
        )
    )
