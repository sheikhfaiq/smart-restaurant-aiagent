import sys
import os

# Add the project root to sys.path to allow imports from 'app'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import base
from app.database.session import SessionLocal
from app.services.agent.agent_builder import SmartAgent
import json

def interactive_chat():
    db = SessionLocal()
    session_id = "terminal_admin_test"
    agent = SmartAgent(db, session_id=session_id)
    
    print("--- Smart Restaurant AI Agent: Interactive Test ---")
    print("Type 'exit' or 'quit' to stop.")
    print("You can ask about the menu, deals, ingredients, or place an order.")
    print("---------------------------------------------------")

    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ["exit", "quit"]:
                break

            # For demo/test, we can inject context here if needed
            # e.g., if message contains "order", we inject some dummy context
            context = None
            if "order" in user_input.lower() and "status" not in user_input.lower():
                 context = {
                    "customerName": "Admin Tester",
                    "phone": "0000000000",
                    "address": "Terminal Test Office",
                    "order_items": [{"menuItemId": 1, "quantity": 1}]
                }
                 print("(Simulating context for order creation...)")

            response = agent.handle_message(user_input, context)
            
            print(f"\nAI ({response['type']}):")
            print(f"{response['message']}")
            
            if response.get('data'):
                print(f"Data: {json.dumps(response['data'], indent=2)}")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\nError: {e}")

    db.close()
    print("\nChat finished. Goodbye!")

if __name__ == "__main__":
    interactive_chat()
