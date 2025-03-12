from collections.abc import Sequence
from datetime import UTC, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, RootModel

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
    root: list[Any]

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


def datetime_now() -> datetime:
    return datetime.now(UTC)


# Should be called Citation, Attribution or Reference but whatever
class QuotationItem(BaseModel, extra="forbid"):
    nid: str  # data source NanoID
    pages: str = Field(default_factory=str)
    timestamp: datetime = Field(default_factory=datetime_now)


class QuotationsSchema(RootModel):
    root: dict[
        str,
        list[QuotationItem]
        | dict[str, list[QuotationItem]]
        | list[list[QuotationItem]],
    ]


class CurrentDateAreaSchema(ListRootModel):
    class CurrentDateAreaItem(BaseModel):
        model_config = ConfigDict(extra="forbid")

        current: bool = False
        date: LooseDateStr | str | None = None
        area: float | None = None

    root: list[CurrentDateAreaItem]


class _CurrentDateAreaChoicesSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    current: bool = False
    date: LooseDateStr | str | None = None
    area: float | None = None

    # Use covariant "Sequence" over invariant "List"
    # see https://mypy.readthedocs.io/en/stable/common_issues.html#variance
    choices: Sequence[Enum]


class CurrentDateAreaChoicesIOI(ListRootModel):
    class CurrentDateAreaChoicesIOIItem(_CurrentDateAreaChoicesSchema):
        choices: list[IntentionOfInvestmentEnum]

    root: list[CurrentDateAreaChoicesIOIItem]


class CurrentDateAreaChoicesCrops(ListRootModel):
    class CurrentDateAreaChoicesCropsItem(_CurrentDateAreaChoicesSchema):
        choices: list[CropsEnum]

    root: list[CurrentDateAreaChoicesCropsItem]


class CurrentDateAreaChoicesAnimals(ListRootModel):
    class CurrentDateAreaChoicesAnimalsItem(_CurrentDateAreaChoicesSchema):
        choices: list[AnimalsEnum]

    root: list[CurrentDateAreaChoicesAnimalsItem]


class _CurrentDateChoiceSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")
    current: bool = False
    date: LooseDateStr | str | None = None
    choice: Enum


class CurrentDateChoiceNegotiationStatus(ListRootModel):
    class CurrentDateChoiceNegotiationStatusItem(_CurrentDateChoiceSchema):
        choice: NegotiationStatusEnum

    root: list[CurrentDateChoiceNegotiationStatusItem]


class CurrentDateChoiceImplementationStatus(ListRootModel):
    class CurrentDateChoiceImplementationStatusItem(_CurrentDateChoiceSchema):
        choice: ImplementationStatusEnum

    root: list[CurrentDateChoiceImplementationStatusItem]


class _ExportsSchema(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )  # turning this off for now because of "yield"

    current: bool = False
    # in the following line, the "str" is intentional (https://github.com/pydantic/pydantic/discussions/8176#discussioncomment-7620012)
    date: LooseDateStr | str | None = None
    choices: Sequence[Enum]

    area: float | None = None
    yield_: float | None = Field(None, alias="yield")
    export: float | None = None


class ExportsCrops(ListRootModel):
    class ExportsCropsItem(_ExportsSchema):
        choices: list[CropsEnum]

    root: list[ExportsCropsItem]


class ExportsAnimals(ListRootModel):
    class ExportsAnimalsItem(_ExportsSchema):
        choices: list[AnimalsEnum]

    root: list[ExportsAnimalsItem]


class ExportsMineralResources(ListRootModel):
    class ExportsMineralResourcesItem(_ExportsSchema):
        choices: list[MineralsEnum]

    root: list[ExportsMineralResourcesItem]


class LeaseSchema(ListRootModel):
    class LeaseItem(BaseModel):
        model_config = ConfigDict(extra="forbid")

        current: bool = False
        date: LooseDateStr | str | None = None
        area: float | None = None
        farmers: int | None = None
        households: int | None = None

    root: list[LeaseItem]


class JobsSchema(ListRootModel):
    class JobsItem(BaseModel):
        model_config = ConfigDict(extra="forbid")

        current: bool = False
        date: LooseDateStr | str | None = None
        jobs: int | None = None
        employees: int | None = None
        workers: int | None = None

    root: list[JobsItem]


class ActorsSchema(ListRootModel):
    class ActorsItem(BaseModel):
        model_config = ConfigDict(extra="forbid")
        name: str
        role: ActorEnum = ActorEnum.OTHER

    root: list[ActorsItem]


class ElectricityGenerationSchema(ListRootModel):
    class ElectricityGenerationItem(BaseModel):
        model_config = ConfigDict(extra="forbid")

        current: bool = False
        date: LooseDateStr | str | None = None
        area: float | None = None
        choices: list[ElectricityGenerationEnum]
        export: float | None = None  # in percent
        windfarm_count: int | None = None
        current_capacity: float | None = None
        intended_capacity: float | None = None

    root: list[ElectricityGenerationItem]


class CarbonSequestrationSchema(ListRootModel):
    class CarbonSequestrationItem(BaseModel):
        model_config = ConfigDict(extra="forbid")

        current: bool = False
        start_date: LooseDateStr | str | None = None
        end_date: LooseDateStr | str | None = None
        area: float | None = None
        choices: list[CarbonSequestrationEnum]
        projected_lifetime_sequestration: float | None = None  # in tCO2e
        projected_annual_sequestration: float | None = None  # in tCO2e
        project_proponents: str = ""
        certification_standard: bool | None = None
        certification_standard_name: list[CarbonSequestrationCertEnum]
        certification_standard_id: str = ""
        certification_standard_comment: str = ""

    root: list[CarbonSequestrationItem]


class WFIReplySchema(ListRootModel):
    class WFIReplyItem(BaseModel):
        model_config = ConfigDict(extra="forbid")

        timestamp: str
        user_id: int
        comment: str

    root: list[WFIReplyItem]
