from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class OrderItemBase(BaseModel):
    menu_item_id: int
    quantity: int

class OrderItemSchema(OrderItemBase):
    id: int
    price: float
    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    customer_name: str
    phone: str
    address: str
    notes: Optional[str] = None

class OrderCreate(OrderBase):
    items: List[OrderItemBase]

class OrderSchema(OrderBase):
    id: int
    order_number: str
    total_amount: float
    status: str
    created_at: datetime
    items: List[OrderItemSchema]
    class Config:
        from_attributes = True
