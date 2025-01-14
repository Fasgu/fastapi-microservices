from typing import List, Optional

from app.models.pydantic import ItemPayloadSchema
from models.item import ItemModel


async def get(id: int) -> Optional[dict]:
    item = await ItemModel.filter(id=id).first().values()
    if item:
        return item[0]
    return None


async def get_all() -> List:
    return await ItemModel.all().values()


async def post(payload: ItemPayloadSchema) -> ItemPayloadSchema:
    item = ItemModel(
        code=payload.code,
        name=payload.name,
        description=payload.description,
        purchase_price=payload.purchase_price,
        sale_price=payload.sale_price
    )
    await item.save()
    return item


async def insert_bulk(payload: List[ItemPayloadSchema]) -> None:
    batch = [ItemModel(
        code=row.code,
        name=row.name,
        description=row.description,
        purchase_price=row.purchase_price,
        sale_price=row.sale_price) for row in payload]

    return await ItemModel.bulk_create(batch)


async def delete(id: int) -> int:
    item = await ItemModel.filter(id=id).first().delete()
    return item


async def put(id: int, payload: ItemPayloadSchema) -> Optional[dict]:
    item = await ItemModel.filter(id=id).update(
        code=payload.code,
        name=payload.name,
        description=payload.description,
        purchase_price=payload.purchase_price,
        sale_price=payload.sale_price
    )
    if item:
        return await get(id)
    return None


async def validate_exists(code: str, name: str) -> bool:
    return await ItemModel.filter(code=code).exists() or await ItemModel.filter(name=name).exists()


async def validate_exists_edit(id: int, code: str, name: str) -> bool:
    return (await ItemModel.filter(code=code).exclude(id=id).exists()
            or await ItemModel.filter(name=name).exclude(id=id).exists())


