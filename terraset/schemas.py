from pydantic import BaseModel, validator, StrictStr

from .configs import (
    supported_superset_objects,
    bases
)

class SupersetObject(BaseModel):
    superset_object: StrictStr

    @validator('superset_object')
    def superset_object_validation(cls, v):
        if len(set([v]).difference(set(supported_superset_objects))) > 0:
            raise ValueError(
                "Valid values are '" + "', '".join(supported_superset_objects) + "'")
        return v

class Bases(BaseModel):
    base: StrictStr

    @validator('base')
    def base_validation(cls, v):
        if len(set([v]).difference(set(bases))) > 0:
            raise ValueError(
                "Valid values are '" + "', '".join(bases) + "'")
        return v
