
from nanoid import generate

from django.db.models import Model


def generate_nid(model: type[Model]) -> str:
    nid = generate(size=8)

    while model.objects.filter(nid=nid).exists():
        nid = generate(size=8)

    return nid


def populate_nid_field(model: type[Model]) -> None:
    for instance in model.objects.all():
        if instance.nid is None:
            instance.nid = generate_nid(model)
            instance.save()


def nullify_nid_field(model: type[Model]) -> None:
    model.objects.update(nid=None)
