from typing import List, Optional
from sqlalchemy.orm import Session
from models.inventory import MovementType, ProductModel, StockModel, StockMovementModel
from schemas.inventory import ProductCreate


def get_product_by_id(db: Session, product_id: int) -> Optional[ProductModel]:
    return db.query(ProductModel).filter(ProductModel.id == product_id).first()


def get_product_by_sku(db: Session, sku: str) -> Optional[ProductModel]:
    return db.query(ProductModel).filter(ProductModel.sku == sku).first()


def list_products(db: Session) -> List[ProductModel]:
    return db.query(ProductModel).order_by(ProductModel.id.asc()).all()


def create_product(db: Session, payload: ProductCreate) -> ProductModel:
    product = ProductModel(
        sku=payload.sku.strip(),
        name=payload.name.strip(),
        description=payload.description.strip() if payload.description else None,
    )
    db.add(product)
    db.flush()

    stock = StockModel(
        product_id=product.id,
        quantity_available=0,
        quantity_reserved=0,
    )
    db.add(stock)
    db.commit()
    db.refresh(product)
    return product


def get_stock_by_product_id(db: Session, product_id: int) -> Optional[StockModel]:
    return db.query(StockModel).filter(StockModel.product_id == product_id).first()


def create_movement(
    db: Session,
    product_id: int,
    movement_type: MovementType,
    quantity: int,
    reference_id: Optional[str] = None,
) -> StockMovementModel:
    movement = StockMovementModel(
        product_id=product_id,
        movement_type=movement_type,
        quantity=quantity,
        reference_id=reference_id.strip() if reference_id else None,
    )
    db.add(movement)
    db.commit()
    db.refresh(movement)
    return movement


def list_movements(db: Session, product_id: Optional[int] = None) -> List[StockMovementModel]:
    query = db.query(StockMovementModel)
    if product_id is not None:
        query = query.filter(StockMovementModel.product_id == product_id)
    return query.order_by(StockMovementModel.id.desc()).all()