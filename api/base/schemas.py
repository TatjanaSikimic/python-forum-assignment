from pydantic import BaseModel as PydanticBaseModel
import humps


def to_camel(string):
    return humps.camelize(string)


# This should be the base model that is inherited
class BaseModel(PydanticBaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
        orm_mode = True

    # TODO: Add configuration that supports camelcase conversion, and also supports regular snake_case assignment, along with camelCase assignment
    # TODO: There should be the function that converts model key names to camelCase (Try to create it yourself, help is also in the README)
