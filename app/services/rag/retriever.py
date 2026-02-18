import psycopg2
from app.config import DATABASE_URL
from app.services.rag.embedding import get_embedding

def retrieve_relevant_docs(question: str, top_k=5):
    embedding = get_embedding(question)
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT content
            FROM documents
            ORDER BY embedding <-> %s::vector
            LIMIT %s
        """, (embedding, top_k))
        
        results = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return results
    except Exception as e:
        print(f"Retrieval Error: {e}")
        if cursor: cursor.close()
        if conn: conn.close()
        return []
