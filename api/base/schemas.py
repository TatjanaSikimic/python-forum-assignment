from pydantic import BaseModel as PydanticBaseModel
from humps.main import camelize


class BaseModel(PydanticBaseModel):
    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True


class Test(BaseModel):
    aa: int
    bb_cc: int
