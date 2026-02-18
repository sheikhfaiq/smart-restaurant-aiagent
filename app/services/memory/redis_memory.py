import redis
import json
from app.config import REDIS_URL

class RedisMemory:
    _local_memory = {}  # In-memory fallback if Redis is down

    def __init__(self):
        try:
            self.redis = redis.from_url(REDIS_URL, decode_responses=True)
            # Ping to verify connection
            self.redis.ping()
            self.use_redis = True
        except Exception as e:
            print(f"⚠️ Redis not available ({e}). Using in-memory fallback.")
            self.redis = None
            self.use_redis = False

    def get_history(self, session_id: str):
        if self.use_redis:
            try:
                history = self.redis.get(f"chat_history:{session_id}")
                return json.loads(history) if history else []
            except Exception:
                self.use_redis = False  # Switching to fallback
        
        return self._local_memory.get(session_id, [])

    def add_message(self, session_id: str, role: str, content: str):
        history = self.get_history(session_id)
        history.append({"role": role, "content": content})
        # Keep last 10 messages
        history = history[-10:]

        if self.use_redis:
            try:
                self.redis.set(f"chat_history:{session_id}", json.dumps(history), ex=3600)
                return
            except Exception:
                self.use_redis = False # Connection lost
        
        self._local_memory[session_id] = history
