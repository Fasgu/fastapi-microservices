from typing import List
from fastapi import APIRouter, status, Path, HTTPException
from app.api import crud
from models.item import ItemSchema
from app.models.pydantic import ItemPayloadSchema, ItemResponseSchema

router = APIRouter(prefix="/items")


@router.get("/{id}/", response_model=ItemSchema)
async def get_item(id: int = Path(..., gt=0)) -> ItemSchema:
    item = await crud.get(id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found!")
    return item


@router.get("/", response_model=List[ItemSchema])
async def get_all_items() -> List[ItemSchema]:
    return await crud.get_all()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_item(payload: ItemPayloadSchema) -> ItemResponseSchema:
    validate_exists = await crud.validate_exists(payload.code, payload.name)

    if validate_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Item with same name already exists!",
        )
    else:
        item = await crud.post(payload)
        return item


@router.delete("/{id}/")
async def delete_item(id: int = Path(..., gt=0)) -> int:
    item = await crud.get(id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found!")
    await crud.delete(id)
    return id


@router.put("/{id}/", response_model=ItemSchema)
async def update_item(payload: ItemPayloadSchema, id: int = Path(..., gt=0)) -> ItemSchema:
    item = await crud.put(id, payload)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found!")
    return item
