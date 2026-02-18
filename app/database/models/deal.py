from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.session import Base

class Deal(Base):
    __tablename__ = "Deal"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    discount = Column(Float, default=0.0)
    isActive = Column(Boolean, default=True)
    startDate = Column(DateTime)
    endDate = Column(DateTime)
    createdAt = Column(DateTime(timezone=True), default=func.now())
    
    menuItems = relationship("DealMenuItem", back_populates="deal")

class DealMenuItem(Base):
    __tablename__ = "DealMenuItem"
    dealId = Column(Integer, ForeignKey("Deal.id"), primary_key=True)
    menuItemId = Column(Integer, ForeignKey("MenuItem.id"), primary_key=True)
    
    deal = relationship("Deal", back_populates="menuItems")
    menuItem = relationship("MenuItem", back_populates="deals")
