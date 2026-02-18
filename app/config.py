import os
from dotenv import load_dotenv

load_dotenv()

# Database
DATABASE_URL = os.getenv("DATABASE_URL")  # Supabase Postgres connection

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Redis (optional for memory)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
