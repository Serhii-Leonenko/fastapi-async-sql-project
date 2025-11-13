from pydantic import BaseModel, ConfigDict

from cheese.models import PackagingType


class CheeseTypeBase(BaseModel):
    name: str
    description: str


class CheeseTypeCreate(CheeseTypeBase):
    pass


class CheeseType(CheeseTypeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class CheeseBase(BaseModel):
    title: str
    price: int
    packaging_type: PackagingType


class CheeseCreate(CheeseBase):
    cheese_type_id: int


class Cheese(CheeseBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cheese_type: CheeseType
