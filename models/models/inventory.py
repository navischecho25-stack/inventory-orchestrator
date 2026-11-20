import enum
from sqlalchemy import Column, DateTime, Enum as SQLEnum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base


class MovementType(str, enum.Enum):
    INBOUND = "INBOUND"
    OUTBOUND = "OUTBOUND"
    ADJUSTMENT = "ADJUSTMENT"


class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(150), nullable=False)
    description = Column(String(300), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    stock = relationship(
        "StockModel",
        back_populates="product",
        uselist=False,
        cascade="all, delete-orphan",
    )
    movements = relationship(
        "StockMovementModel",
        back_populates="product",
        cascade="all, delete-orphan",
    )


class StockModel(Base):
    __tablename__ = "inventory_stock"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), unique=True, nullable=False)
    quantity_available = Column(Integer, nullable=False, default=0)
    quantity_reserved = Column(Integer, nullable=False, default=0)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    product = relationship("ProductModel", back_populates="stock")


class StockMovementModel(Base):
    __tablename__ = "stock_movements"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    movement_type = Column(SQLEnum(MovementType), nullable=False)
    quantity = Column(Integer, nullable=False)
    reference_id = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    product = relationship("ProductModel", back_populates="movements")