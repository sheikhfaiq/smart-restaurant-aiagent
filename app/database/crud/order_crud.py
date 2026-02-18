from sqlalchemy.orm import Session
from app.database.models.order import Order, OrderItem, OrderStatusEnum
from app.database.models.menu_item import MenuItem
import uuid

def create_order(db: Session, customer_name: str, phone: str, address: str, items: list):
    order_number = str(uuid.uuid4())[:8]
    total_amount = 0
    order_items = []

    for item in items:
        menu_item_id = item.get("menu_item_id") or item.get("menuItemId")
        quantity = item.get("quantity")
        
        menu_item = db.query(MenuItem).filter(MenuItem.id == menu_item_id).first()
        if not menu_item:
            continue
        item_price = menu_item.price * quantity
        total_amount += item_price
        order_items.append(OrderItem(menuItemId=menu_item.id, quantity=quantity, price=item_price))

    order = Order(
        orderNumber=order_number,
        customerName=customer_name,
        phone=phone,
        address=address,
        totalAmount=total_amount,
        items=order_items
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def update_order_items(db: Session, order: Order, new_items: list):
    """Adds items to an existing order if it's PENDING or CONFIRMED."""
    if order.status not in [OrderStatusEnum.PENDING, OrderStatusEnum.CONFIRMED]:
        return None
        
    for item in new_items:
        menu_item_id = item.get("menu_item_id") or item.get("menuItemId")
        quantity = item.get("quantity")
        
        menu_item = db.query(MenuItem).filter(MenuItem.id == menu_item_id).first()
        if not menu_item:
            continue
            
        item_price = menu_item.price * quantity
        order.totalAmount += item_price
        
        # Check if item already exists in order to combine quantities
        existing_item = next((oi for oi in order.items if oi.menuItemId == menu_item_id), None)
        if existing_item:
            existing_item.quantity += quantity
            existing_item.price += item_price
        else:
            order.items.append(OrderItem(menuItemId=menu_item_id, quantity=quantity, price=item_price))
            
    db.commit()
    db.refresh(order)
    return order

def get_order_by_number(db: Session, order_number: str):
    return db.query(Order).filter(Order.orderNumber == order_number).first()

def get_active_order_by_phone(db: Session, phone: str):
    """Returns the most recent PENDING or CONFIRMED order for a phone number."""
    return db.query(Order).filter(
        Order.phone == phone,
        Order.status.in_([OrderStatusEnum.PENDING, OrderStatusEnum.CONFIRMED])
    ).order_by(Order.createdAt.desc()).first()
