from typing import List, Optional
from sqlalchemy.orm import Session
from models.inventory import MovementType, ProductModel, StockModel, StockMovementModel
from repositories import inventory as inventory_repo
from schemas.inventory import MovementCreate, ProductCreate


def register_product(db: Session, payload: ProductCreate) -> ProductModel:
    normalized_sku = payload.sku.strip()
    existing = inventory_repo.get_product_by_sku(db, normalized_sku)
    if existing is not None:
        raise ValueError(f"Product with SKU '{normalized_sku}' already exists.")

    clean_payload = ProductCreate(
        sku=normalized_sku,
        name=payload.name.strip(),
        description=payload.description.strip() if payload.description else None,
    )
    return inventory_repo.create_product(db, clean_payload)


def get_product_or_raise(db: Session, product_id: int) -> ProductModel:
    product = inventory_repo.get_product_by_id(db, product_id)
    if product is None:
        raise ValueError(f"Product with ID {product_id} not found.")
    return product


def get_all_products(db: Session) -> List[ProductModel]:
    return inventory_repo.list_products(db)


def get_stock_or_raise(db: Session, product_id: int) -> StockModel:
    get_product_or_raise(db, product_id)
    stock = inventory_repo.get_stock_by_product_id(db, product_id)
    if stock is None:
        stock = StockModel(
            product_id=product_id,
            quantity_available=0,
            quantity_reserved=0,
        )
        db.add(stock)
        db.commit()
        db.refresh(stock)
    return stock


def record_movement(db: Session, payload: MovementCreate) -> StockMovementModel:
    stock = get_stock_or_raise(db, payload.product_id)

    try:
        if payload.movement_type == MovementType.INBOUND:
            stock.quantity_available += payload.quantity

        elif payload.movement_type == MovementType.OUTBOUND:
            if stock.quantity_available < payload.quantity:
                raise ValueError(
                    f"Insufficient available stock: requested {payload.quantity}, "
                    f"available {stock.quantity_available}."
                )
            stock.quantity_available -= payload.quantity

        elif payload.movement_type == MovementType.ADJUSTMENT:
            if payload.quantity < 0:
                raise ValueError("Adjustment quantity cannot be negative.")
            stock.quantity_available = payload.quantity

        movement = StockMovementModel(
            product_id=payload.product_id,
            movement_type=payload.movement_type,
            quantity=payload.quantity,
            reference_id=payload.reference_id.strip() if payload.reference_id else None,
        )
        db.add(movement)
        db.commit()
        db.refresh(movement)
        db.refresh(stock)
        return movement

    except Exception:
        db.rollback()
        raise


def get_movements(
    db: Session, product_id: Optional[int] = None
) -> List[StockMovementModel]:
    if product_id is not None:
        get_product_or_raise(db, product_id)
    return inventory_repo.list_movements(db, product_id=product_id)