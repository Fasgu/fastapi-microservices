from typing import Optional
from pydantic import BaseModel


class ItemPayloadSchema(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    purchase_price: float
    sale_price: float


class ItemResponseSchema(ItemPayloadSchema):
    id: int
