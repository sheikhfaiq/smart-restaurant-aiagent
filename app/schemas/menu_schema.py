from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    is_available: bool = True

class MenuItemSchema(MenuItemBase):
    id: int
    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    name: str
    slug: str

class CategorySchema(CategoryBase):
    id: int
    menu_items: List[MenuItemSchema] = []
    class Config:
        from_attributes = True
