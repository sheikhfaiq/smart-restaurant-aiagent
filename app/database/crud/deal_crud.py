from sqlalchemy.orm import Session
from app.database.models.deal import Deal

def get_active_deals(db: Session):
    return db.query(Deal).filter(Deal.isActive == True).all()

# Prisma schema doesn't show promoCode, but if needed, we'd add it to the model first.
# For now, let's just use what's in the Prisma schema provided.
