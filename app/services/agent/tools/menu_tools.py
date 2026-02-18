from sqlalchemy.orm import Session
from app.database.crud import menu_crud
from app.database.models.menu_item import MenuItem

def list_menu(db: Session, category: str = None):
    # 1. Try to find items by category
    items = menu_crud.get_menu_items(db, category)
    
    # 2. If nothing found and category was provided, try searching by item name
    if not items and category:
        items = db.query(MenuItem).filter(
            MenuItem.name.ilike(f"%{category}%"),
            MenuItem.isAvailable == True
        ).all()
        
    if not items:
        if category:
            return f"Sorry, we couldn't find any items in our '{category}' category or matching that name."
        return "Sorry, we couldn't find any items on the menu right now."
    
    response = "🍴 Our Menu:\n"
    for item in items:
        # Use price formatting
        price = f"${item.price:.2f}" if item.price else "Price N/A"
        response += f"- {item.name}: {item.description} ({price})\n"
    return response

def get_item_details(db: Session, name: str):
    item = menu_crud.get_menu_item_by_name(db, name)
    if item:
        price = f"${item.price:.2f}" if item.price else "N/A"
        return f"{item.name}: {item.description}. Price: {price}."
    return "I couldn't find that specific item on the menu."
