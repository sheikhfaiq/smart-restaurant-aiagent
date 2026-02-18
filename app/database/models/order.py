from sqlalchemy import Column, Integer, String, Float, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database.session import Base

class OrderStatusEnum(str, enum.Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    PREPARING = "PREPARING"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

class Order(Base):
    __tablename__ = "Order"
    id = Column(Integer, primary_key=True, index=True)
    orderNumber = Column(String, unique=True, nullable=False)
    customerName = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=False)
    notes = Column(String)
    totalAmount = Column(Float)
    status = Column(Enum(OrderStatusEnum), default=OrderStatusEnum.PENDING)
    createdAt = Column(DateTime(timezone=True), default=func.now())
    updatedAt = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "OrderItem"
    id = Column(Integer, primary_key=True, index=True)
    orderId = Column(Integer, ForeignKey("Order.id"))
    menuItemId = Column(Integer, ForeignKey("MenuItem.id"))
    quantity = Column(Integer)
    price = Column(Float)
    
    order = relationship("Order", back_populates="items")
    menuItem = relationship("MenuItem", back_populates="orderItems")
