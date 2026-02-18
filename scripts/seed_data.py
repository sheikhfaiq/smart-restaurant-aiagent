from sqlalchemy.orm import Session
from app.database.session import SessionLocal, engine, Base
from app.database.models.category import Category
from app.database.models.menu_item import MenuItem
from app.database.models.deal import Deal
from app.database.base import metadata

def seed_data():
    # Create tables
    metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Check if data exists
    if db.query(Category).first():
        print("Data already exists. Skipping seed.")
        return

    # Categories
    burgers = Category(name="Burger", slug="burger")
    drinks = Category(name="Drink", slug="drink")
    db.add_all([burgers, drinks])
    db.commit()

    # Menu Items
    items = [
        MenuItem(name="Zinger Burger", slug="zinger", description="Crispy chicken fillet with lettuce and mayo", price=5.99, category_id=burgers.id),
        MenuItem(name="Beef Whopper", slug="whopper", description="Flame-grilled beef with veggies", price=7.49, category_id=burgers.id),
        MenuItem(name="Coca Cola", slug="coke", description="Ice cold refreshment", price=1.99, category_id=drinks.id),
    ]
    db.add_all(items)
    
    # Deals
    deals = [
        Deal(title="Lunch Special", description="20% off on all burgers", discount_percentage=20.0, promo_code="LUNCH20"),
        Deal(title="Welcome Deal", description="Get $2 off your first order", discount_percentage=10.0, promo_code="WELCOME10"),
    ]
    db.add_all(deals)
    
    db.commit()
    db.close()
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_data()
