from typing import List, Optional

from app.models.pydantic import PersonPayloadSchema
from models.person import PersonModel


async def get(id: int) -> Optional[dict]:
    person = await PersonModel.filter(id=id).first().values()
    if person:
        return person[0]
    return None


async def get_all(type: str) -> List:
    return await PersonModel.filter(type=type).values()


async def post(payload: PersonPayloadSchema) -> PersonPayloadSchema:
    person = PersonModel(
        type=payload.type,
        document_type=payload.document_type,
        document_number=payload.document_number,
        name=payload.name,
        address=payload.address
    )
    await person.save()
    return person


async def delete(id: int) -> int:
    person = await PersonModel.filter(id=id).first().delete()
    return person


async def put(id: int, payload: PersonPayloadSchema) -> Optional[dict]:
    person = await PersonModel.filter(id=id).update(
        document_type=payload.document_type,
        document_number=payload.document_number,
        name=payload.name,
        address=payload.address
    )
    if person:
        return await get(id)
    return None


async def validate_exists(type: str, document_type: str, document_number: str) -> bool:
    return await PersonModel.filter(type=type).filter(document_type=document_type)\
        .filter(document_number=document_number).exists()


async def validate_exists_edit(id: int, type: str, document_type: str, document_number: str) -> bool:
    return await PersonModel.filter(type=type).filter(document_type=document_type)\
        .filter(document_number=document_number)\
        .exclude(id=id)\
        .exists()

