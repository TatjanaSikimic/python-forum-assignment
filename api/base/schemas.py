from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    pass

    # TODO: Add configuration that supports camelcase conversion, and also supports regular snake_case assignment, along with camelCase assignment
    # TODO: There should be the function that converts model key names to camelCase (Try to create it yourself, help is also in the README)
