import json
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from openai import OpenAI
from app.config import OPENAI_API_KEY
from app.services.agent.tools import menu_tools, order_tools, deal_tools, rag_tool
from app.services.memory.redis_memory import RedisMemory
from app.services.agent.prompts.system_prompt import SYSTEM_PROMPT
from app.database.models.menu_item import MenuItem
from app.database.crud import order_crud

client = OpenAI(api_key=OPENAI_API_KEY)

class SmartAgent:
    def __init__(self, db: Session, session_id: str = "default"):
        self.db = db
        self.session_id = session_id
        self.memory = RedisMemory()

    def _get_history_context(self) -> str:
        history = self.memory.get_history(self.session_id)
        if not history:
            return "No previous conversation history."
        
        context = "Full Conversation History (for context):\n"
        for msg in history:
            role = "User" if msg["role"] == "user" else "Assistant"
            context += f"{role}: {msg['content']}\n"
        return context

    def _get_active_order_context(self, phone: str = None) -> str:
        """Checks for active orders and returns a summary for the LLM."""
        if not phone:
            # Try to find phone in history
            history = self.memory.get_history(self.session_id)
            for msg in reversed(history):
                # Simple heuristic to find a phone-like number in previous messages
                import re
                found = re.search(r'\d{7,15}', msg["content"])
                if found:
                    phone = found.group()
                    break
        
        if phone:
            active_order = order_crud.get_active_order_by_phone(self.db, phone)
            if active_order:
                items = ", ".join([f"{oi.menuItem.name} x{oi.quantity}" for oi in active_order.items])
                return f"\n[ACTIVE ORDER FOUND: Order #{active_order.orderNumber}, Status: {active_order.status.value}, Items: {items}, Total: ${active_order.totalAmount:.2f}]\n"
        
        return "\n[NO ACTIVE ORDER FOUND]\n"

    def _map_items_to_ids(self, item_names: List[str]) -> List[Dict[str, Any]]:
        """Maps natural language item names to database MenuItem IDs."""
        order_items = []
        if not item_names:
            return []
            
        for name in item_names:
            item = self.db.query(MenuItem).filter(MenuItem.name.ilike(f"%{name}%"), MenuItem.isAvailable == True).first()
            if item:
                found = False
                for oi in order_items:
                    if oi["menuItemId"] == item.id:
                        oi["quantity"] += 1
                        found = True
                        break
                if not found:
                    order_items.append({
                        "menuItemId": item.id, 
                        "quantity": 1, 
                        "name": item.name, 
                        "price": item.price
                    })
        return order_items

    def _analyze_conversation(self, message: str) -> Dict[str, Any]:
        history = self._get_history_context()
        order_context = self._get_active_order_context()
        
        prompt = f"""
        {SYSTEM_PROMPT}

        CORE ANALYTICS TASK:
        Analyze the USER MESSAGE in the context of the CONVERSATION HISTORY and the ACTIVE ORDER STATUS below.
        
        {order_context}

        CONVERSATION HISTORY:
        {history}

        CURRENT USER MESSAGE:
        "{message}"

        JSON RESPONSE FORMAT:
        {{
            "intent": "browse_menu" | "check_deals" | "start_order" | "track_order" | "faq_query" | "provide_info" | "confirm_order" | "cancel_order" | "greeting",
            "entities": {{
                "name": "Customer name",
                "phone": "Phone number",
                "address": "Delivery address",
                "items": ["Item 1", "Item 2"],
                "category": "Extracted category",
                "orderNumber": "Order number"
            }},
            "bot_response": "GENERATE THE FINAL RESPONSE MESSAGE HERE following ALL system guidelines. If an active order is found, acknowledge that you will add to it if the user wants more items.",
            "needs_tool": true/false
        }}
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": "You are a professional restaurant AI assistant. Reply ONLY with valid JSON."}, 
                         {"role": "user", "content": prompt}],
                response_format={ "type": "json_object" }
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Analysis Error: {e}")
            return {"intent": "faq_query", "entities": {}, "bot_response": "I'm sorry, I encountered an error.", "needs_tool": False}

    def handle_message(self, message: str, user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        # 1. Save message to history
        self.memory.add_message(self.session_id, "user", message)
        
        # 2. Analyze full context
        analysis = self._analyze_conversation(message)
        intent = analysis.get("intent")
        entities = analysis.get("entities", {})
        bot_msg = analysis.get("bot_response", "")
        needs_tool = analysis.get("needs_tool", False)
        
        response = {"type": "text", "message": bot_msg, "data": None}

        if needs_tool:
            if intent == "browse_menu":
                category = entities.get("category")
                tool_output = menu_tools.list_menu(self.db, category)
                response["message"] = f"{bot_msg}\n\n{tool_output}"
                response["type"] = "menu"
            elif intent == "check_deals":
                tool_output = deal_tools.format_deals(self.db)
                response["message"] = f"{bot_msg}\n\n{tool_output}"
                response["type"] = "deals"
            elif intent == "track_order":
                order_num = entities.get("orderNumber")
                if order_num:
                    tool_output = order_tools.track_order(self.db, order_num)
                    response["message"] = f"{bot_msg}\n{tool_output}"
                    response["type"] = "order_status"

        elif intent == "confirm_order":
            name = entities.get("name")
            phone = entities.get("phone")
            address = entities.get("address")
            items_raw = entities.get("items", [])
            mapped_items = self._map_items_to_ids(items_raw)

            if name and phone and address and mapped_items:
                try:
                    order_result = order_tools.create_new_order(self.db, {
                        "customer_name": name,
                        "phone": phone,
                        "address": address,
                        "order_items": mapped_items
                    })
                    response["type"] = "order_created"
                    response["message"] = f"{bot_msg}\n\n{order_result}"
                except Exception as e:
                    response["message"] = "I apologize, but I hit a snag placing your order. Please try again."
                    print(f"Order Error: {e}")
            else:
                # Fallback: Something is missing even though LLM thought it was confirmation time
                missing = []
                if not name: missing.append("name")
                if not phone: missing.append("phone number")
                if not address: missing.append("address")
                if not mapped_items: missing.append("items")
                
                response["message"] = f"I'd love to finalize that for you, but I'm still missing your **{', '.join(missing)}**. Could you please provide those?"

        elif intent == "faq_query":
            try:
                answer = rag_tool.generate_answer(message)
                response["type"] = "knowledge"
                response["message"] = answer
            except Exception:
                response["message"] = "I'm not exactly sure about that. Would you like to see our menu?"

        self.memory.add_message(self.session_id, "assistant", response["message"])
        return response
