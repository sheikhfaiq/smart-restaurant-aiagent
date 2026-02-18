from sqlalchemy.orm import Session
from app.database.crud import order_crud

def create_new_order(db: Session, context: dict):
    customer_name = context.get("customer_name", "Guest")
    phone = context.get("phone")
    address = context.get("address")
    items = context.get("orderItems") or context.get("order_items") or []

    if not phone or not address or not items:
        return "I need your phone number, address, and items to place an order."

    # Check for an existing active order (PENDING/CONFIRMED)
    active_order = order_crud.get_active_order_by_phone(db, phone)
    
    if active_order:
        # Update existing order instead of creating a new one
        updated_order = order_crud.update_order_items(db, active_order, items)
        if updated_order:
            return f"I've added those items to your existing order #{updated_order.orderNumber}! Your new total is ${updated_order.totalAmount:.2f}."
        else:
            # This case shouldn't happen based on the filter, but good for safety
            return "Your order is already being prepared and cannot be modified. I can start a new order for you if you'd like!"

    # Create new order if no active one exists
    order = order_crud.create_order(db, customer_name, phone, address, items)
    return f"Order #{order.orderNumber} created successfully! Total: ${order.totalAmount:.2f}"

def track_order(db: Session, order_number: str):
    order = order_crud.get_order_by_number(db, order_number)
    if order:
        return f"Order #{order.orderNumber} status: {order.status.value}. Total: ${order.totalAmount:.2f}"
    return f"I couldn't find an order with number #{order_number}."
