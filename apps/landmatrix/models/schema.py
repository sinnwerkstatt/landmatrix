from datetime import datetime
from decimal import Decimal
from typing import List

from pydantic import BaseModel, ConfigDict, Extra, Field, RootModel

from apps.landmatrix.models.choices import (
    ActorEnum,
    AnimalsEnum,
    CarbonSequestrationCertEnum,
    CarbonSequestrationEnum,
    CropsEnum,
    ElectricityGenerationEnum,
    ImplementationStatusEnum,
    IntentionOfInvestmentEnum,
    MineralsEnum,
    NegotiationStatusEnum,
)


class ListRootModel(RootModel):
    root: List[None]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    # def __iadd__(self, other):
    #     self.root += other
    #     return self
    #
    # def append(self, value):
    #     self.root.append(value)


class LooseDateStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value: str, _info):
        date_formats = ["%Y-%m-%d", "%Y-%m", "%Y"]
        for date_format in date_formats:
            try:
                datetime.strptime(value, date_format)
                return cls(value)  # Cast the validated value back into LooseDateStr
            except ValueError:
                continue
        raise ValueError(
            "Invalid date format. Please use 'yyyy-mm-dd', 'yyyy-mm', or 'yyyy'."
        )


class CurrentDateAreaSchema(ListRootModel):
    class CurrentDateAreaItem(BaseModel):
        model_config = ConfigDict(extra=Extra.forbid)

        current: bool = False
        date: LooseDateStr | str | None = None
        area: Decimal

    root: List[CurrentDateAreaItem]


class _CurrentDateAreaChoicesSchema(BaseModel):
    model_config = ConfigDict(extra=Extra.forbid)
    current: bool = False
    date: LooseDateStr | str | None = None
    area: Decimal | None = None
    choices: list[str]


class CurrentDateAreaChoicesIOI(ListRootModel):
    class CurrentDateAreaChoicesIOIItem(_CurrentDateAreaChoicesSchema):
        choices: list[IntentionOfInvestmentEnum]

    root: List[CurrentDateAreaChoicesIOIItem]


class CurrentDateAreaChoicesCrops(ListRootModel):
    class CurrentDateAreaChoicesCropsItem(_CurrentDateAreaChoicesSchema):
        choices: list[CropsEnum]

    root: List[CurrentDateAreaChoicesCropsItem]


class CurrentDateAreaChoicesAnimals(ListRootModel):
    class CurrentDateAreaChoicesAnimalsItem(_CurrentDateAreaChoicesSchema):
        choices: list[AnimalsEnum]

    root: List[CurrentDateAreaChoicesAnimalsItem]


class _CurrentDateChoiceSchema(BaseModel):
    model_config = ConfigDict(extra=Extra.forbid)
    current: bool = False
    date: LooseDateStr | str | None = None
    choice: str


class CurrentDateChoiceNegotiationStatus(ListRootModel):
    class CurrentDateChoiceNegotiationStatusItem(_CurrentDateChoiceSchema):
        choice: NegotiationStatusEnum

    root: List[CurrentDateChoiceNegotiationStatusItem]


class CurrentDateChoiceImplementationStatus(ListRootModel):
    class CurrentDateChoiceImplementationStatusItem(_CurrentDateChoiceSchema):
        choice: ImplementationStatusEnum

    root: List[CurrentDateChoiceImplementationStatusItem]


class _ExportsSchema(BaseModel):
    model_config = ConfigDict(
        extra=Extra.forbid, populate_by_name=True
    )  # turning this off for now because of "yield"

    current: bool = False
    # in the following line, the "str" is intentional (https://github.com/pydantic/pydantic/discussions/8176#discussioncomment-7620012)
    date: LooseDateStr | str | None = None
    choices: list[str]
    area: Decimal | None = None
    yield_: Decimal | None = Field(None, alias="yield")
    export: Decimal | None = None


class ExportsCrops(ListRootModel):
    class ExportsCropsItem(_ExportsSchema):
        choices: list[CropsEnum]

    root: List[ExportsCropsItem]


class ExportsAnimals(ListRootModel):
    class ExportsAnimalsItem(_ExportsSchema):
        choices: list[AnimalsEnum]

    root: List[ExportsAnimalsItem]


class ExportsMineralResources(ListRootModel):
    class ExportsMineralResourcesItem(_ExportsSchema):
        choices: list[MineralsEnum]

    root: List[ExportsMineralResourcesItem]


class LeaseSchema(ListRootModel):
    class LeaseItem(BaseModel):
        model_config = ConfigDict(extra=Extra.forbid)
        current: bool = False
        date: LooseDateStr | str | None = None
        area: Decimal | None = None
        farmers: Decimal | None = None
        households: Decimal | None = None

    root: List[LeaseItem]


class JobsSchema(ListRootModel):
    class JobsItem(BaseModel):
        model_config = ConfigDict(extra=Extra.forbid)
        current: bool = False
        date: LooseDateStr | str | None = None
        jobs: Decimal | None = None
        employees: Decimal | None = None
        workers: Decimal | None = None

    root: List[JobsItem]


class ActorsSchema(ListRootModel):
    class ActorsItem(BaseModel):
        model_config = ConfigDict(extra=Extra.forbid)
        name: str
        role: ActorEnum = ActorEnum.OTHER

    root: List[ActorsItem]


class ElectricityGenerationSchema(ListRootModel):
    class ElectricityGenerationItem(BaseModel):
        model_config = ConfigDict(extra=Extra.forbid)
        current: bool = False
        date: LooseDateStr | str | None = None
        area: Decimal | None = None
        choices: list[ElectricityGenerationEnum] = []
        export: Decimal | None = None
        windfarm_count: Decimal | None = None
        current_capacity: Decimal | None = None
        intended_capacity: Decimal | None = None

    root: List[ElectricityGenerationItem]


class CarbonSequestrationSchema(ListRootModel):
    class CarbonSequestrationItem(BaseModel):
        model_config = ConfigDict(extra=Extra.forbid)
        current: bool = False
        date: LooseDateStr | str | None = None
        area: Decimal | None = None
        choices: list[CarbonSequestrationEnum] = []
        projected_lifetime_sequestration: Decimal | None = None
        projected_annual_sequestration: Decimal | None = None
        certification_standard: bool | None = None
        certification_standard_name: CarbonSequestrationCertEnum | None = None
        certification_standard_id: str = ""
        certification_standard_comment: str = ""

    root: List[CarbonSequestrationItem]
