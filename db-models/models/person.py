from tortoise import fields, models
from enum import Enum
from tortoise.contrib.pydantic import pydantic_model_creator


class Type(str, Enum):
    CUSTOMER = "C"
    SUPPLIER = "S"


class DocumentType(str, Enum):
    DNI = "1"
    RUC = "6"


class PersonModel(models.Model):
    type = fields.CharEnumField(Type)
    document_type = fields.CharEnumField(DocumentType)
    document_number = fields.TextField(max_length=11)
    name = fields.TextField(max_length=255)
    address = fields.TextField(null=True)
    active = fields.BooleanField(default=True)

    def __str__(self):
        return self.name


PersonSchema = pydantic_model_creator(PersonModel)
