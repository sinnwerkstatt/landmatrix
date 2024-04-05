from django_pydantic_field.rest_framework import SchemaField
from drf_spectacular.utils import extend_schema_field

from apps.landmatrix.models import schema


@extend_schema_field(schema.CurrentDateAreaSchema)
class CurrentDateAreaSchemaField(SchemaField):
    def __init__(self, *args, **kwargs):
        super().__init__(schema=schema.CurrentDateAreaSchema, *args, **kwargs)


@extend_schema_field(schema.CurrentDateAreaChoicesIOI)
class CurrentDateAreaChoicesIOIField(SchemaField):
    def __init__(self, *args, **kwargs):
        super().__init__(schema=schema.CurrentDateAreaChoicesIOI, *args, **kwargs)


@extend_schema_field(schema.CurrentDateChoiceNegotiationStatus)
class CurrentDateChoiceNegotiationStatusField(SchemaField):
    def __init__(self, *args, **kwargs):
        super().__init__(
            schema=schema.CurrentDateChoiceNegotiationStatus, *args, **kwargs
        )


@extend_schema_field(schema.CurrentDateChoiceImplementationStatus)
class CurrentDateChoiceImplementationStatusField(SchemaField):
    def __init__(self, *args, **kwargs):
        super().__init__(
            schema=schema.CurrentDateChoiceImplementationStatus, *args, **kwargs
        )


@extend_schema_field(schema.LeaseSchema)
class LeaseSchemaField(SchemaField):
    def __init__(self, *args, **kwargs):
        super().__init__(schema=schema.LeaseSchema, *args, **kwargs)


@extend_schema_field(schema.JobsSchema)
class JobsSchemaField(SchemaField):
    def __init__(self, *args, **kwargs):
        super().__init__(schema=schema.JobsSchema, *args, **kwargs)


@extend_schema_field(schema.ActorsSchema)
class ActorsSchemaField(SchemaField):
    def __init__(self, *args, **kwargs):
        super().__init__(schema=schema.ActorsSchema, *args, **kwargs)


@extend_schema_field(schema.ExportsCrops)
class CropsSchemaField(SchemaField):
    def __init__(self, *args, **kwargs):
        super().__init__(schema=schema.ExportsCrops, *args, **kwargs)


@extend_schema_field(schema.ExportsAnimals)
class ExportsAnimalsField(SchemaField):
    def __init__(self, *args, **kwargs):
        super().__init__(schema=schema.ExportsAnimals, *args, **kwargs)


@extend_schema_field(schema.ExportsMineralResources)
class ExportsMineralResourcesField(SchemaField):
    def __init__(self, *args, **kwargs):
        super().__init__(schema=schema.ExportsMineralResources, *args, **kwargs)


@extend_schema_field(schema.CurrentDateAreaChoicesCrops)
class CurrentDateAreaChoicesCropsField(SchemaField):
    def __init__(self, *args, **kwargs):
        super().__init__(schema=schema.CurrentDateAreaChoicesCrops, *args, **kwargs)


@extend_schema_field(schema.CurrentDateAreaChoicesAnimals)
class CurrentDateAreaChoicesAnimalsField(SchemaField):
    def __init__(self, *args, **kwargs):
        super().__init__(schema=schema.CurrentDateAreaChoicesAnimals, *args, **kwargs)


@extend_schema_field(schema.ElectricityGenerationSchema)
class ElectricityGenerationSchemaField(SchemaField):
    def __init__(self, *args, **kwargs):
        super().__init__(schema=schema.ElectricityGenerationSchema, *args, **kwargs)


@extend_schema_field(schema.CarbonSequestrationSchema)
class CarbonSequestrationSchemaField(SchemaField):
    def __init__(self, *args, **kwargs):
        super().__init__(schema=schema.CarbonSequestrationSchema, *args, **kwargs)
