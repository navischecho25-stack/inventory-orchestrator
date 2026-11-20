from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.inventory import (
    MovementCreate,
    MovementResponse,
    ProductCreate,
    ProductResponse,
    StockResponse,
)
from services import inventory as inventory_service

router = APIRouter(tags=["Inventory"])


@router.post(
    "/products",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product_endpoint(
    payload: ProductCreate,
    db: Session = Depends(get_db),
):
    try:
        return inventory_service.register_product(db, payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get("/products", response_model=List[ProductResponse])
def list_products_endpoint(db: Session = Depends(get_db)):
    return inventory_service.get_all_products(db)


@router.get("/products/{product_id}/stock", response_model=StockResponse)
def get_product_stock_endpoint(
    product_id: int,
    db: Session = Depends(get_db),
):
    try:
        return inventory_service.get_stock_or_raise(db, product_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.post(
    "/movements",
    response_model=MovementResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_movement_endpoint(
    payload: MovementCreate,
    db: Session = Depends(get_db),
):
    try:
        return inventory_service.record_movement(db, payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get("/movements", response_model=List[MovementResponse])
def list_movements_endpoint(
    product_id: Optional[int] = Query(default=None, gt=0),
    db: Session = Depends(get_db),
):
    try:
        return inventory_service.get_movements(db, product_id=product_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc