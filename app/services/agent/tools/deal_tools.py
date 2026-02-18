from sqlalchemy.orm import Session
from app.database.crud import deal_crud

def format_deals(db: Session):
    deals = deal_crud.get_active_deals(db)
    if not deals:
        return "No active deals at the moment."
    
    response = "🎉 Here are our current deals:\n"
    for deal in deals:
        response += f"- {deal.title}: {deal.description} (Save ${deal.discount})\n"
    return response

# Note: check_promo removed because promoCode is not in the existing Prisma schema.
