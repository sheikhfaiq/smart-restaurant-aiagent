from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.session import Base

class MenuItem(Base):
    __tablename__ = "MenuItem"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    description = Column(String)
    price = Column(Float)
    image = Column(String)
    isPopular = Column(Boolean, default=False)
    isAvailable = Column(Boolean, default=True)
    categoryId = Column(Integer, ForeignKey("Category.id"))
    createdAt = Column(DateTime(timezone=True), default=func.now())
    updatedAt = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    category = relationship("Category", back_populates="menuItems")
    orderItems = relationship("OrderItem", back_populates="menuItem")
    deals = relationship("DealMenuItem", back_populates="menuItem")
