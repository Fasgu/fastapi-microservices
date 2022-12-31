from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from fastapi import APIRouter, status, Path, HTTPException
from app.api import crud
from models.person import PersonSchema
from app.models.pydantic import PersonPayloadSchema, PersonResponseSchema

router = APIRouter(prefix="/persons")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@router.get("/detail/{id}/", response_model=PersonSchema)
async def get_person(id: int = Path(..., gt=0)) -> PersonSchema:
    return await get_person_validation(id)


@router.get("/{type}/", response_model=List[PersonSchema])
async def get_all_persons(type: str) -> List[PersonSchema]:
    return await crud.get_all(type)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_person(payload: PersonPayloadSchema) -> PersonResponseSchema:
    validate_exists = await crud.validate_exists(payload.type, payload.document_type, payload.document_number)

    if validate_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Person with same document number already exists!",
        )
    else:
        person = await crud.post(payload)
        return person


@router.delete("/{id}/")
async def delete_person(id: int = Path(..., gt=0)) -> int:
    await get_person_validation(id)
    await crud.delete(id)
    return id


@router.put("/{id}/", response_model=PersonSchema)
async def update_person(payload: PersonPayloadSchema, id: int = Path(..., gt=0)) -> PersonSchema:
    await get_person_validation(id)

    validate_exists = await crud.validate_exists_edit(
        id, payload.type, payload.document_type, payload.document_number
    )

    if validate_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Person with same document number already exists!",
        )
    person = await crud.put(id, payload)
    return person


async def get_person_validation(id):
    person = await crud.get(id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found!")

    return person
