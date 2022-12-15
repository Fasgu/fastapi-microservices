from typing import Optional
from pydantic import BaseModel, ValidationError, validator


class PersonPayloadSchema(BaseModel):
    type: str
    document_type: str
    document_number: str
    name: str
    address: Optional[str] = None

    @validator('type')
    def validate_type(cls, value):
        if value not in ["C", "S"]:
            raise ValueError("field 'type' must be one of 'C', 'S'")
        return value

    @validator('document_type')
    def validate_document_type(cls, value):
        if value not in ["1", "6"]:
            raise ValueError("field 'document_type' must be one of '1', '6'")
        return value


class PersonResponseSchema(PersonPayloadSchema):
    id: int
