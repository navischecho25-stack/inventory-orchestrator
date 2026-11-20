from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from models.inventory import MovementType


class ProductCreate(BaseModel):
    sku: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=150)
    description: Optional[str] = Field(default=None, max_length=300)


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sku: str
    name: str
    description: Optional[str] = None
    created_at: datetime


class StockResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    quantity_available: int
    quantity_reserved: int
    updated_at: datetime


class MovementCreate(BaseModel):
    product_id: int = Field(..., gt=0)
    movement_type: MovementType
    quantity: int = Field(..., gt=0)
    reference_id: Optional[str] = Field(default=None, max_length=100)


class MovementResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    movement_type: MovementType
    quantity: int
    reference_id: Optional[str] = None
    created_at: datetime