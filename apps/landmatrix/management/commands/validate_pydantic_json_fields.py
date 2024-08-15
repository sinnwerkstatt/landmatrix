from django.core.exceptions import ValidationError
from tqdm import tqdm

from django.core.management import BaseCommand

from apps.landmatrix.models.deal import DealVersion
from django_pydantic_jsonfield import PydanticJSONField

pydantic_json_fields = [
    field for field in DealVersion._meta.fields if isinstance(field, PydanticJSONField)
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        total = DealVersion.objects.count()
        iterator = DealVersion.objects.iterator()

        print("Iterating DealVersions.")
        for version in tqdm(iterator, total=total):
            for field in pydantic_json_fields:
                try:
                    field.run_validators(getattr(version, field.name))
                except ValidationError as e:
                    print("ERROR", version, field.name, "".join(m for m in e))

        print("DONE")
