from sqlalchemy.orm import Session
from app.database.models.menu_item import MenuItem
from app.database.models.category import Category

def get_menu_items(db: Session, category_name: str = None):
    query = db.query(MenuItem).filter(MenuItem.isAvailable == True)
    if category_name:
        # Use case-insensitive partial match for categories
        query = query.join(MenuItem.category).filter(Category.name.ilike(f"%{category_name}%"))
    return query.all()

def get_menu_item_by_name(db: Session, name: str):
    # Use case-insensitive partial match for items
    return db.query(MenuItem).filter(MenuItem.name.ilike(f"%{name}%"), MenuItem.isAvailable == True).first()
