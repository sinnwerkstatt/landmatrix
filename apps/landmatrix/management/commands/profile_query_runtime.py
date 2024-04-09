import json
from typing import Type

from django.core.management import BaseCommand
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import ForeignKey, Model
from django.forms import model_to_dict

from apps.landmatrix.models.deal import DealOld, DealVersionOld, DealWorkflowInfoOld
from apps.landmatrix.models.investor import (
    InvestorOld,
    InvestorVersionOld,
    InvestorWorkflowInfoOld,
)


from timeit import default_timer


class Timer:
    """Custom Timer class."""

    def __init__(self, name: str):
        self._name = name
        self._start_time = None

    def __enter__(self):
        """Start a new timer as a context manager"""
        self._start_time = default_timer()
        return self

    def __exit__(self, *exc_info):
        """Stop the context manager timer"""
        duration = default_timer() - self._start_time
        self._start_time = None

        print(f"Runtime {self._name}: {duration:0.3f}s")

# Todo?! exchange deal old
MODELS: list[Type[Model]] = [
    DealOld,
    DealVersionOld,
    DealWorkflowInfoOld,
    InvestorOld,
    InvestorVersionOld,
    InvestorWorkflowInfoOld,
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        """Run queryset profiler."""
        for model in MODELS:
            profile_query_runtime(model)


def profile_query_runtime(
    model: Type[Model],
    limit: int | None = None,
):
    print()
    print(f"### {model.__name__} ###")
    print(f"Count: {model.objects.count()}")

    with Timer(f"objects.all()"):
        list(model.objects.all()[:limit])

    with Timer(f"map(model_to_dict, objects.all())"):
        list(map(model_to_dict, model.objects.all()[:limit]))

    with Timer(f"objects.values()"):
        list(model.objects.values()[:limit])

    # NOTES:
    # i) model.object.values()
    #
    # * ForeignKey -> { '<fk_field_name>_id': int }
    # * no ManyToManyField relations
    # * DateTimeField -> { '<dt_field_name>': datetime.datetime }
    dict_db = model.objects.values().first()

    # i) map(model_to_dict, model.objects.all())
    #
    # * ForeignKey -> { '<fk_field_name>': id }
    # * ManyToManyField as objs -> { '<m2m_field_name>': [<related_obj>] }
    # * DateTimeField -> { '<dt_field_name>': datetime.datetime }
    dict_m2d = model_to_dict(model.objects.first())

    # the two dicts are equal except
    # * dict_db names fk_fields as '<fk_field_name>_id' and dict_m2d as '<fk_name>'
    # * dict_db does not contain m2m_fields

    # compare_dicts(dict_db, dict_m2d)
    assert filter_and_map_keys(dict_m2d, model) == dict_db

    # Both, dict_db and dict_m2d, can contain class instances as values
    # ->  not json serializable by default
    # ->  use django.core.serializers.json.DjangoJSONEncoder

    json.dumps(
        dict_db,
        sort_keys=True,
        indent=2,
        cls=DjangoJSONEncoder,
    )


def filter_and_map_keys(d: dict, model: Type[Model]):
    return {
        k + "_id" if k in get_fk_fields(model) else k: v
        for k, v in d.items()
        if k not in get_m2m_fields(model)
    }


def get_fk_fields(model: Type[Model]):
    fk_field_objs = filter(lambda x: isinstance(x, ForeignKey), model._meta.fields)
    return list(map(lambda x: x.name, fk_field_objs))


def get_m2m_fields(model: Type[Model]):
    return list(map(lambda x: x.name, model._meta.many_to_many))


def compare_dicts(d1: dict, d2: dict):
    not_in_d2 = [k1 for k1 in d1.keys() if k1 not in d2.keys()]
    not_in_d1 = [k2 for k2 in d2.keys() if k2 not in d1.keys()]

    print("Not in first:", not_in_d1)
    print("Not in second:", not_in_d2)
